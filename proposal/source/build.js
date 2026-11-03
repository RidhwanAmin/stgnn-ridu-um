const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, ImageRun, Footer, PageNumber, LineNumberRestartFormat, PageBreak,
  BorderStyle, VerticalAlign, TabStopType,
} = require("docx");

const FONT = "Times New Roman";
const TEXT_W = 11906 - 2268 - 1134; // A4 width minus 4 cm left and 2 cm right (DXA)
const lines = fs.readFileSync("content.txt", "utf8").split("\n");

function runs(text, base = {}) {
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*)/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    const tok = m[0];
    if (tok.startsWith("**")) out.push(new TextRun({ text: tok.slice(2, -2), bold: true, ...base }));
    else out.push(new TextRun({ text: tok.slice(1, -1), italics: true, ...base }));
    last = m.index + tok.length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out;
}

const body = (text) => new Paragraph({ children: runs(text), alignment: AlignmentType.JUSTIFIED, spacing: { line: 480, after: 120 } });

function makeTable(caption, widths, rows) {
  const ws = widths.map((w) => Math.round((w / 100) * TEXT_W));
  ws[ws.length - 1] += TEXT_W - ws.reduce((a, b) => a + b, 0);
  const cap = new Paragraph({ children: runs(caption, { bold: true }), keepNext: true, spacing: { line: 276, before: 240, after: 120 } });
  const trs = rows.map((cells, ri) => new TableRow({
    tableHeader: ri === 0,
    cantSplit: true,
    children: cells.map((c, ci) => new TableCell({
      width: { size: ws[ci], type: WidthType.DXA },
      shading: ri === 0 ? { type: ShadingType.CLEAR, color: "auto", fill: "EDEDED" } : undefined,
      margins: { top: 60, bottom: 60, left: 90, right: 90 },
      verticalAlign: VerticalAlign.TOP,
      children: [new Paragraph({
        children: runs(c, { size: 20, bold: ri === 0 }),
        alignment: c.trim() === "■" ? AlignmentType.CENTER : AlignmentType.LEFT,
        spacing: { line: 240 },
      })],
    })),
  }));
  const table = new Table({ width: { size: TEXT_W, type: WidthType.DXA }, columnWidths: ws, rows: trs });
  return [cap, table, new Paragraph({ children: [], spacing: { after: 120 } })];
}

function makeFigure(file, widthCm, caption) {
  const buf = fs.readFileSync(file);
  const w = buf.readUInt32BE(16), h = buf.readUInt32BE(20);
  const px = Math.round((widthCm / 2.54) * 96);
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 240 },
      children: [new ImageRun({ type: "png", data: buf, transformation: { width: px, height: Math.round((px * h) / w) },
        altText: { title: caption, description: caption, name: file } })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, children: runs(caption, { bold: false }), spacing: { line: 276, before: 120, after: 240 } }),
  ];
}

const children = [];
let i = 0, inRefs = false;
while (i < lines.length) {
  const raw = lines[i];
  const line = raw.trimEnd();
  if (!line.trim()) { i++; continue; }
  if (line === "PAGEBREAK") { children.push(new Paragraph({ children: [new PageBreak()] })); i++; continue; }
  if (line === "ABSTRACT") {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, alignment: AlignmentType.CENTER, children: [new TextRun({ text: "ABSTRACT" })] }));
    i++; continue;
  }
  if (line.startsWith("# ")) {
    const t = line.slice(2);
    inRefs = t === "REFERENCES";
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, alignment: AlignmentType.CENTER, children: [new TextRun({ text: t })] }));
    i++; continue;
  }
  if (line.startsWith("## ")) { children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun({ text: line.slice(3) })] })); i++; continue; }
  if (line.startsWith("TABLE|")) {
    const caption = line.slice(6);
    const widths = lines[i + 1].slice(2).split("|").map(Number);
    const rows = [];
    i += 2;
    while (lines[i].trim() !== "ENDTABLE") { rows.push(lines[i].split(" | ").map((s) => s.replace(/\s*\|\s*$/, "").trim())); i++; }
    rows.forEach((r, k) => { while (r.length < widths.length) r.push(""); rows[k] = r.slice(0, widths.length); });
    children.push(...makeTable(caption, widths, rows));
    i++; continue;
  }
  if (line.startsWith("FIGURE|")) {
    const [, file, wcm, ...cap] = line.split("|");
    children.push(...makeFigure(file, Number(wcm), cap.join("|")));
    i++; continue;
  }
  if (line.startsWith("EQ|")) {
    const parts = line.split("|"); const num = parts.pop(); const eq = parts.slice(1).join("|");
    children.push(new Paragraph({
      tabStops: [{ type: TabStopType.CENTER, position: Math.round(TEXT_W / 2) }, { type: TabStopType.RIGHT, position: TEXT_W }],
      spacing: { line: 360, before: 120, after: 120 },
      children: [new TextRun({ text: "\t" + eq, italics: true }), new TextRun({ text: "\t(" + num + ")" })],
    }));
    i++; continue;
  }
  if (line.startsWith("REF|")) {
    children.push(new Paragraph({ children: runs(line.slice(4)), indent: { left: 720, hanging: 720 }, spacing: { line: 480, after: 0 } }));
    i++; continue;
  }
  children.push(body(line));
  i++;
}

const tp = (text, opts = {}) => new Paragraph({ suppressLineNumbers: true, alignment: AlignmentType.CENTER, spacing: { line: 360, after: opts.after ?? 0, before: opts.before ?? 0 },
  children: [new TextRun({ text, bold: !!opts.bold, size: opts.size ?? 24, font: FONT })] });

const titlePage = [
  tp("UNIVERSITI MALAYA", { bold: true, after: 120 }),
  tp("Faculty of Computer Science and Information Technology", { after: 1200 }),
  tp("ESTIMATING ATRIAL ECTOPY BURDEN FROM SMARTWATCH BEAT INTERVALS: A TWO-SCALE SPATIO-TEMPORAL GRAPH NEURAL NETWORK AND ITS FEASIBILITY IN POST-STROKE SURVIVORS", { bold: true, size: 28, after: 1200 }),
  tp("RESEARCH PROPOSAL", { bold: true, after: 120 }),
  tp("Submitted for the Proposal Defence", { after: 1200 }),
  tp("RIDHWAN AMIN AZHARI BIN ZABIDI", { bold: true, after: 60 }),
  tp("Matric No.: 25118475", { after: 60 }),
  tp("Doctor of Philosophy (by Research)", { after: 1000 }),
  tp("Supervisors", { bold: true, after: 60 }),
  tp("Dr. Bryan Raj A/L Peter Jabaraj", { after: 60 }),
  tp("Associate Prof. Ts. Dr. Ismail Bin Ahmedy", { after: 1000 }),
  tp("2026"),
];

const doc = new Document({
  creator: "Ridhwan Amin Azhari Bin Zabidi",
  title: "Research Proposal: Estimating Atrial Ectopy Burden from Smartwatch Beat Intervals",
  styles: {
    default: { document: { run: { font: FONT, size: 24 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 24, bold: true, color: "000000" },
        paragraph: { spacing: { before: 240, after: 240, line: 480 }, keepNext: true, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { font: FONT, size: 24, bold: true, color: "000000" },
        paragraph: { spacing: { before: 240, after: 120, line: 480 }, keepNext: true, outlineLevel: 1 } },
    ],
  },
  sections: [
    { properties: { page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, right: 1134, bottom: 1134, left: 2268 } } },
      footers: { default: new Footer({ children: [new Paragraph({ suppressLineNumbers: true, children: [] })] }) },
      children: titlePage },
    { properties: {
        page: { size: { width: 11906, height: 16838 }, margin: { top: 1134, right: 1134, bottom: 1134, left: 2268 },
          pageNumbers: { start: 1 } },
        lineNumbers: { countBy: 1, restart: LineNumberRestartFormat.CONTINUOUS },
      },
      footers: { default: new Footer({ children: [new Paragraph({ suppressLineNumbers: true, alignment: AlignmentType.CENTER,
        children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 24 })] })] }) },
      children },
  ],
});

Packer.toBuffer(doc).then((b) => { fs.writeFileSync("Ridhwan_Research_Proposal_UM.docx", b); console.log("written"); });
