import * as pdfjsLib from 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.4.168/pdf.min.mjs';

pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/4.4.168/pdf.worker.min.mjs';
const REQUIRED = ['Number','X','Y','Z','Z_Toe','Length','Azimuth','Angle','DesignCharge','Stemming','Subdrilling','DetonatingTime'];
const OUTPUT = [['Plano','plan_id'],['Tipo','plan_type_label'],['id','Number'],['y','Y'],['x','X'],['z (crest)','Z'],['z (toe)','Z_Toe'],['profundidade prevista','Length'],['azimute','Azimuth'],['inclinacao','Angle'],['cargas previstas','DesignCharge'],['tampao previsto','Stemming'],['subperfuracao','Subdrilling'],['diametro','Diameter'],['DetonatingTime','DetonatingTime']];
const state = { files: [], output: null, planType: null };
const $ = id => document.getElementById(id);
const dropzone = $('dropzone'), input = $('file-input'), fileList = $('file-list'), generate = $('generate-button');

function setProgress(message, value) { $('progress-message').textContent = message; $('progress-value').textContent = `${value}%`; $('progress-bar').style.width = `${value}%`; }
function fail(message) { $('error-box').hidden = false; $('error-box').textContent = message; setProgress('A execução foi interrompida.', 0); }
function clearError() { $('error-box').hidden = true; $('error-box').textContent = ''; }
function ext(file) { return file.name.split('.').pop().toLowerCase(); }
function renderFiles() { fileList.innerHTML = state.files.length ? state.files.map((file, i) => `<span class="file-chip"><b>${ext(file).toUpperCase()}</b><span>${escapeHtml(file.name)}</span><button type="button" data-remove="${i}" aria-label="Remover ${escapeHtml(file.name)}">×</button></span>`).join('') : '<span class="empty-files">Nenhum arquivo selecionado</span>'; generate.disabled = !state.files.some(f => ext(f) === 'csv'); }
function escapeHtml(value) { return value.replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c])); }
function addFiles(files) { const incoming = [...files]; const names = new Set(state.files.map(f => f.name)); state.files = [...state.files, ...incoming.filter(f => !names.has(f.name))]; clearError(); renderFiles(); setProgress(`${state.files.length} arquivo(s) selecionado(s).`, 0); }
dropzone.addEventListener('click', () => input.click());
dropzone.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); input.click(); } });
input.addEventListener('change', e => addFiles(e.target.files));
['dragenter','dragover'].forEach(event => dropzone.addEventListener(event, e => { e.preventDefault(); dropzone.classList.add('is-dragging'); }));
['dragleave','drop'].forEach(event => dropzone.addEventListener(event, e => { e.preventDefault(); dropzone.classList.remove('is-dragging'); }));
dropzone.addEventListener('drop', e => addFiles(e.dataTransfer.files));
fileList.addEventListener('click', e => { const button = e.target.closest('[data-remove]'); if (button) { state.files.splice(Number(button.dataset.remove), 1); renderFiles(); } });

function readText(file) { return new Promise((resolve, reject) => { const reader = new FileReader(); reader.onload = () => resolve(String(reader.result)); reader.onerror = () => reject(new Error(`Falha ao ler ${file.name}.`)); reader.readAsText(file); }); }
async function readPdfText(file) { const pdf = await pdfjsLib.getDocument({ data: await file.arrayBuffer() }).promise; let text = ''; for (let i = 1; i <= pdf.numPages; i++) { const page = await pdf.getPage(i); const content = await page.getTextContent(); text += `${content.items.map(item => item.str).join(' ')}\n`; if (/(?:PP|PC)\s*\d{6,7}/i.test(text)) break; } return text; }
function normalizeId(raw) { return String(raw).replace(/^0+/, '') || '0'; }
function extractId(text) { const match = String(text ?? '').match(/\b(?:PP|PC)\s*0*(\d{6,7})\b/i); return match ? normalizeId(match[1]) : null; }
function detectType(files, rows) { const match = files.map(f => f.name).join(' ').match(/\b(PP|PC)\b/i) || String(rows?.[0]?.Number || '').match(/^(PP|PC)/i); return match ? match[1].toUpperCase() : 'PP'; }
function number(value, label) { const parsed = Number(String(value ?? '').trim().replace(',', '.')); if (!Number.isFinite(parsed)) throw new Error(`Valor numérico inválido em ${label}: “${value}”.`); return parsed; }
function parseCsvText(text) { const records = []; let row = [], cell = '', quoted = false; for (let i = 0; i < text.length; i++) { const char = text[i], next = text[i + 1]; if (char === '"') { if (quoted && next === '"') { cell += '"'; i++; } else quoted = !quoted; } else if (char === ',' && !quoted) { row.push(cell); cell = ''; } else if ((char === '\n' || char === '\r') && !quoted) { if (char === '\r' && next === '\n') i++; row.push(cell); if (row.some(value => value.trim() !== '')) records.push(row); row = []; cell = ''; } else cell += char; } if (cell.length || row.length) { row.push(cell); records.push(row); } if (!records.length) return []; const headers = records.shift().map(header => header.replace(/^\uFEFF/, '').trim()); return records.map(values => Object.fromEntries(headers.map((header, index) => [header, (values[index] ?? '').trim()]))); }
async function parseCsv(file) { const rows = parseCsvText(await readText(file)); return rows; }
async function parseWorkbook(file) { const wb = XLSX.read(await file.arrayBuffer(), { type: 'array', cellDates: false }); let map = new Map(), foundId = null; for (const sheetName of wb.SheetNames) { const rows = XLSX.utils.sheet_to_json(wb.Sheets[sheetName], { header: 1, defval: null }); for (const row of rows) { for (const cell of row) { const id = extractId(cell ?? ''); if (id) foundId = id; } const headers = row.map(v => String(v ?? '').trim()); const idIdx = headers.indexOf('ID'), diameterIdx = headers.indexOf('Diameter'); if (idIdx >= 0 && diameterIdx >= 0) { for (const data of rows.slice(rows.indexOf(row) + 1)) if (data[idIdx] != null && data[diameterIdx] != null) map.set(String(data[idIdx]), data[diameterIdx]); } } } return { map, foundId }; }
async function resolveId(files, workbook) { const candidates = []; for (const file of files) { const nameId = extractId(file.name); if (nameId) candidates.push(nameId); if (ext(file) === 'pdf') { const pdfId = extractId(await readPdfText(file)); if (pdfId) candidates.push(pdfId); } } if (workbook.foundId) candidates.push(workbook.foundId); const unique = [...new Set(candidates)]; if (!unique.length) throw new Error('Não foi possível determinar o ID do plano. Use um PDF/XLSX com o identificador PP ou PC.'); if (unique.length > 1) throw new Error(`IDs de plano conflitantes encontrados: ${unique.join(', ')}.`); return unique[0]; }
function validateRows(rows) { if (!rows.length) throw new Error('O CSV não contém linhas de dados.'); const missing = REQUIRED.filter(c => !(c in rows[0])); if (missing.length) throw new Error(`CSV sem colunas obrigatórias: ${missing.join(', ')}.`); rows.forEach((row, i) => { const n = number(row.Number, `Number na linha ${i + 2}`); if (!Number.isInteger(n) || n <= 0) throw new Error(`Number inválido na linha ${i + 2}: esperado inteiro positivo.`); }); }
function buildOutput(rows, diameterMap, planId, planType) { const label = planType === 'PC' ? 'Presplit' : 'Production'; return rows.map(row => { const out = {}; for (const [name, source] of OUTPUT) { if (source === 'plan_id') out[name] = planId; else if (source === 'plan_type_label') out[name] = label; else if (source === 'Number') out[name] = String(row[source]); else if (source === 'Diameter') out[name] = number(diameterMap.get(String(row.Number)), `Diameter do furo ${row.Number}`); else out[name] = number(row[source], `${source} do furo ${row.Number}`); } return out; }); }
function formatOutput(rows) { return rows.map(row => { for (const key of Object.keys(row)) if (typeof row[key] === 'number') { const precision = key === 'x' || key === 'y' ? 4 : key === 'DetonatingTime' ? 0 : 1; row[key] = Number(row[key].toFixed(precision)); } return row; }); }
function applyNumberFormats(sheet, headers, rowCount) { headers.forEach((header, columnIndex) => { const precision = header === 'x' || header === 'y' ? 4 : header === 'DetonatingTime' ? 0 : 1; const format = `0${precision ? `.${'0'.repeat(precision)}` : ''}`; for (let rowIndex = 2; rowIndex <= rowCount + 1; rowIndex++) { const cell = sheet[XLSX.utils.encode_cell({ r: rowIndex - 1, c: columnIndex })]; if (cell && typeof cell.v === 'number') cell.z = format; } }); }
function showResult(rows, planId, planType) { const totalCharge = rows.reduce((sum, row) => sum + Number(row['cargas previstas'] || 0), 0); $('metric-plan').textContent = planId; $('metric-type').textContent = planType === 'PC' ? 'Presplit' : 'Production'; $('metric-holes').textContent = rows.length.toLocaleString('pt-BR'); $('metric-charge').textContent = `${totalCharge.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })} kg`; $('output-name').textContent = state.output.name; $('result-card').hidden = false; }
generate.addEventListener('click', async () => { clearError(); generate.disabled = true; try { setProgress('Lendo o CSV de perfuração…', 20); const csv = state.files.find(f => ext(f) === 'csv'); const rows = await parseCsv(csv); validateRows(rows); setProgress('Lendo o XLSX auxiliar…', 45); const xlsx = state.files.find(f => ['xlsx','xls'].includes(ext(f))); if (!xlsx) throw new Error('XLSX auxiliar ausente: ele é necessário para extrair Diameter.'); const workbook = await parseWorkbook(xlsx); const planId = await resolveId(state.files, workbook); const planType = detectType(state.files, rows); setProgress('Montando DADOS_FUROS e validando saída…', 75); const outputRows = formatOutput(buildOutput(rows, workbook.map, planId, planType)); const headers = OUTPUT.map(([name]) => name); const sheet = XLSX.utils.json_to_sheet(outputRows, { header: headers }); sheet['!cols'] = headers.map(() => ({ wch: 15 })); applyNumberFormats(sheet, headers, outputRows.length); const outBook = XLSX.utils.book_new(); XLSX.utils.book_append_sheet(outBook, sheet, 'DADOS_FUROS'); const bytes = XLSX.write(outBook, { bookType: 'xlsx', type: 'array', compression: true }); state.output = { name: `${planType}${planId}_PREV.xlsx`, bytes }; setProgress('Concluído. O Excel está pronto para baixar.', 100); showResult(outputRows, planId, planType); } catch (error) { fail(error.message || String(error)); } finally { generate.disabled = false; } });
$('download-button').addEventListener('click', () => { if (!state.output) return; const blob = new Blob([state.output.bytes], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }); const link = document.createElement('a'); link.href = URL.createObjectURL(blob); link.download = state.output.name; link.click(); URL.revokeObjectURL(link.href); });
function validateBundleSelection() {
  const allowed = new Set(['csv', 'xlsx', 'xls', 'pdf', 'txt']);
  const unsupported = state.files.filter(file => !allowed.has(ext(file)));
  if (unsupported.length) throw new Error(`Formato não suportado: ${unsupported.map(file => file.name).join(', ')}.`);
  const csvFiles = state.files.filter(file => ext(file) === 'csv');
  if (csvFiles.length !== 1) throw new Error(csvFiles.length ? 'Selecione apenas um CSV de perfuração.' : 'Anexe um CSV de perfuração para continuar.');
  const workbookFiles = state.files.filter(file => ['xlsx', 'xls'].includes(ext(file)));
  if (workbookFiles.length !== 1) throw new Error(workbookFiles.length ? 'Selecione apenas um XLSX auxiliar.' : 'Anexe um XLSX auxiliar com ID e Diameter.');
}
function typeFromText(text) { const match = String(text ?? '').match(/\b(PP|PC)\s*(?=0*\d{6,7}\b)/i); return match ? match[1].toUpperCase() : null; }
async function resolveIdStrict(files, workbook) {
  const candidates = [], types = [];
  for (const file of files) {
    const nameId = extractId(file.name); if (nameId) candidates.push(nameId);
    const nameType = typeFromText(file.name); if (nameType) types.push(nameType);
    if (ext(file) === 'pdf') { const text = await readPdfText(file); const pdfId = extractId(text); if (pdfId) candidates.push(pdfId); const pdfType = typeFromText(text); if (pdfType) types.push(pdfType); }
    if (ext(file) === 'txt') { const text = await readText(file); const txtId = extractId(text); if (txtId) candidates.push(txtId); const txtType = typeFromText(text); if (txtType) types.push(txtType); }
  }
  if (workbook.foundId) candidates.push(workbook.foundId);
  const uniqueIds = [...new Set(candidates)], uniqueTypes = [...new Set(types)];
  if (!uniqueIds.length) throw new Error('Não foi possível determinar o ID do plano. Use um PDF, TXT ou XLSX com o identificador PP ou PC.');
  if (uniqueIds.length > 1) throw new Error(`IDs de plano conflitantes encontrados: ${uniqueIds.join(', ')}.`);
  if (uniqueTypes.length > 1) throw new Error(`Tipos de plano conflitantes encontrados: ${uniqueTypes.join(', ')}.`);
  state.planType = uniqueTypes[0] || null;
  return uniqueIds[0];
}
const originalDetectType = detectType;
resolveId = resolveIdStrict;
detectType = (files, rows) => state.planType || originalDetectType(files, rows);
function prepareGeneration(event) {
  $('progress-panel').hidden = false; $('result-card').hidden = true; state.output = null; state.planType = null;
  try { validateBundleSelection(); } catch (error) { event.preventDefault(); event.stopImmediatePropagation(); generate.disabled = false; fail(error.message); }
}
renderFiles();
$('generate-button').addEventListener('click', prepareGeneration, { capture: true });
input.addEventListener('change', () => { $('result-card').hidden = true; state.output = null; });
fileList.addEventListener('click', () => { $('result-card').hidden = true; state.output = null; });
