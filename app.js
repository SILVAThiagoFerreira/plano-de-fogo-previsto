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
function detectType(files, rows) { if (state.planType) return state.planType; const match = files.map(f => f.name).join(' ').match(/(?:^|[^A-Z])(PP|PC)(?![A-Z])/i) || String(rows?.[0]?.Number || '').match(/^(PP|PC)/i); return match ? match[1].toUpperCase() : 'PP'; }
function number(value, label) { const parsed = Number(String(value ?? '').trim().replace(',', '.')); if (!Number.isFinite(parsed)) throw new Error(`Valor numérico inválido em ${label}: “${value}”.`); return parsed; }
function parseCsvText(text) { const records = []; let row = [], cell = '', quoted = false; for (let i = 0; i < text.length; i++) { const char = text[i], next = text[i + 1]; if (char === '"') { if (quoted && next === '"') { cell += '"'; i++; } else quoted = !quoted; } else if (char === ',' && !quoted) { row.push(cell); cell = ''; } else if ((char === '\n' || char === '\r') && !quoted) { if (char === '\r' && next === '\n') i++; row.push(cell); if (row.some(value => value.trim() !== '')) records.push(row); row = []; cell = ''; } else cell += char; } if (cell.length || row.length) { row.push(cell); records.push(row); } if (!records.length) return { headers: [], rows: [] }; const headers = records.shift().map(header => header.replace(/^\uFEFF/, '').trim()); return { headers, rows: records.map(values => Object.fromEntries(headers.map((header, index) => [header, (values[index] ?? '').trim()]))) }; }
async function parseCsv(file) { return parseCsvText(await readText(file)); }
async function parseWorkbook(file) { const wb = XLSX.read(await file.arrayBuffer(), { type: 'array', cellDates: false }); let map = new Map(), collars = new Map(), foundId = null, names = []; for (const sheetName of wb.SheetNames) { const rows = XLSX.utils.sheet_to_json(wb.Sheets[sheetName], { header: 1, defval: null }); names.push(...workbookNames(rows)); for (const row of rows) { for (const cell of row) { const id = extractId(cell ?? ''); if (id) foundId = id; } const headers = row.map(v => String(v ?? '').trim()); const idIdx = headers.indexOf('ID'), diameterIdx = headers.indexOf('Diameter'); if (idIdx >= 0 && diameterIdx >= 0) { for (const data of rows.slice(rows.indexOf(row) + 1)) if (data[idIdx] != null && data[diameterIdx] != null) map.set(String(data[idIdx]), data[diameterIdx]); } const xIdx = headers.indexOf('X Collar'), yIdx = headers.indexOf('Y Collar'), zIdx = headers.indexOf('Z Collar'); if (idIdx >= 0 && xIdx >= 0 && yIdx >= 0 && zIdx >= 0) { for (const data of rows.slice(rows.indexOf(row) + 1)) { const x = parseNum(data[xIdx]), y = parseNum(data[yIdx]), z = parseNum(data[zIdx]); if (data[idIdx] != null && x !== null && y !== null && z !== null) collars.set(idKey(data[idIdx]), { x, y, z }); } } } } return { map, collars, foundId, names }; }
function validateRows(rows) { if (!rows.length) throw new Error('O CSV não contém linhas de dados.'); const missing = REQUIRED.filter(c => !(c in rows[0])); if (missing.length) throw new Error(`CSV sem colunas obrigatórias: ${missing.join(', ')}.`); rows.forEach((row, i) => { const n = number(row.Number, `Number na linha ${i + 2}`); if (!Number.isInteger(n) || n <= 0) throw new Error(`Number inválido na linha ${i + 2}: esperado inteiro positivo.`); }); }
function buildOutput(rows, planId, planType) { const label = planType === 'PC' ? 'Presplit' : 'Production'; return rows.map(row => { const out = {}; for (const [name, source] of OUTPUT) { if (source === 'plan_id') out[name] = planId; else if (source === 'plan_type_label') out[name] = label; else if (source === 'Number') out[name] = String(row[source]); else if (source === 'DetonatingTime' && /^\s*-?\s*$/.test(String(row[source] ?? ''))) out[name] = null; else out[name] = number(row[source], `${source} do furo ${row.Number}`); } return out; }); }
function formatOutput(rows) { return rows.map(row => { for (const key of Object.keys(row)) if (typeof row[key] === 'number') { const precision = key === 'x' || key === 'y' ? 4 : key === 'DetonatingTime' ? 0 : 1; row[key] = Number(row[key].toFixed(precision)); } return row; }); }
function applyNumberFormats(sheet, headers, rowCount) { headers.forEach((header, columnIndex) => { const precision = header === 'x' || header === 'y' ? 4 : header === 'DetonatingTime' ? 0 : 1; const format = `0${precision ? `.${'0'.repeat(precision)}` : ''}`; for (let rowIndex = 2; rowIndex <= rowCount + 1; rowIndex++) { const cell = sheet[XLSX.utils.encode_cell({ r: rowIndex - 1, c: columnIndex })]; if (cell && typeof cell.v === 'number') cell.z = format; } }); }
function showResult(rows, planId, planType, notices = []) { const totalCharge = rows.reduce((sum, row) => sum + Number(row['cargas previstas'] || 0), 0); $('metric-plan').textContent = planId; $('metric-type').textContent = planType === 'PC' ? 'Presplit' : 'Production'; $('metric-holes').textContent = rows.length.toLocaleString('pt-BR'); $('metric-charge').textContent = `${totalCharge.toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })} kg`; $('output-name').textContent = state.output.name; $('notice-box').innerHTML = notices.map(notice => `<p style="margin:0 0 4px">${escapeHtml(notice)}</p>`).join(''); $('notice-box').hidden = !notices.length; $('result-card').hidden = false; }
const DRILLING_KEYS = ['Number', 'X', 'Y', 'Z', 'Z_Toe', 'DetonatingTime'];
const Z_TOLERANCE = 50;
const INCH_IN_METERS = 0.0254;
function parseNum(value) { const text = String(value ?? '').trim(); if (!text) return null; const parsed = Number(text.replace(',', '.')); return Number.isFinite(parsed) ? parsed : null; }
function idKey(value) { return String(value ?? '').trim(); }
function formatRanges(ids) { const nums = [...new Set(ids.map(Number))].sort((a, b) => a - b); const parts = []; for (let i = 0; i < nums.length;) { let j = i; while (j + 1 < nums.length && nums[j + 1] === nums[j] + 1) j++; parts.push(j > i ? `${nums[i]}–${nums[j]}` : `${nums[i]}`); i = j + 1; } return parts.join(', '); }
// Identifica cada CSV pelo cabeçalho (nunca pelo nome do arquivo).
async function classifyCsvFiles(files) {
  const drilling = [], planned = [], unknown = [];
  for (const file of files.filter(f => ext(f) === 'csv')) {
    const { headers, rows } = await parseCsv(file);
    if (DRILLING_KEYS.every(key => headers.includes(key))) drilling.push({ file, rows });
    else if (headers.includes('Number') && headers.includes('Stemming_m')) planned.push({ file, rows });
    else unknown.push(file.name);
  }
  if (!drilling.length) throw new Error(`Nenhum CSV de perfuração reconhecido (precisa das colunas ${DRILLING_KEYS.join(', ')}).${unknown.length ? ` CSV não reconhecido: ${unknown.join(', ')}.` : ''}`);
  if (drilling.length > 1) throw new Error(`Mais de um CSV de perfuração reconhecido: ${drilling.map(item => item.file.name).join(', ')}.`);
  if (planned.length > 1) throw new Error(`Mais de um CSV de tampão previsto (coluna Stemming_m): ${planned.map(item => item.file.name).join(', ')}.`);
  if (unknown.length) throw new Error(`CSV não reconhecido: ${unknown.join(', ')}. Use o CSV de perfuração (${DRILLING_KEYS.join(', ')}) ou o CSV previsto (Number, Stemming_m).`);
  return { drilling: drilling[0].rows, planned: planned[0]?.rows ?? null };
}
function plannedStemmingMap(rows) { const map = new Map(); for (const row of rows) { const value = parseNum(row.Stemming_m); if (value !== null) map.set(idKey(row.Number), value); } return map; }
// Furo com Z plausível: a cota não pode estar a menos de 50 m de X ou Y, nem acima de 10000.
function hasPlausibleZ(row) { const z = parseNum(row.Z), x = parseNum(row.X), y = parseNum(row.Y); return z !== null && Math.abs(z) <= 10000 && (x === null || Math.abs(z - x) >= Z_TOLERANCE) && (y === null || Math.abs(z - y) >= Z_TOLERANCE); }
// Média ponderada por 1/d² dos 3 furos do XLSX mais próximos (bancada plana).
function estimateCollarZ(x, y, collars) { const nearest = [...collars.values()].map(c => ({ d: Math.hypot(c.x - x, c.y - y), z: c.z })).sort((a, b) => a.d - b.d).slice(0, 3); if (nearest[0].d < 1e-6) return nearest[0].z; const weights = nearest.map(n => 1 / (n.d * n.d)); return nearest.reduce((sum, n, i) => sum + weights[i] * n.z, 0) / weights.reduce((a, b) => a + b, 0); }
function prepareRows(drillingRows, workbook, plannedMap, notices) {
  const zFromXlsx = [], zEstimated = [], zDivergent = [], zMissing = [], diameterFallback = [], stemmingPlanned = [], stemmingFallback = [];
  const rows = drillingRows.map(source => {
    const row = { ...source }, id = idKey(row.Number);
    const z = number(row.Z, `Z do furo ${id}`), zToe = number(row.Z_Toe, `Z_Toe do furo ${id}`);
    const collar = workbook.collars.get(id);
    let crest = null;
    if (!hasPlausibleZ(row)) {
      if (collar) { crest = collar.z; zFromXlsx.push(id); }
      else if (workbook.collars.size) { crest = estimateCollarZ(number(row.X, `X do furo ${id}`), number(row.Y, `Y do furo ${id}`), workbook.collars); zEstimated.push(id); }
      else zMissing.push(id);
    } else if (collar && Math.abs(z - collar.z) > Z_TOLERANCE) { crest = collar.z; zDivergent.push(id); }
    if (crest !== null) { row.Z_Toe = crest - (z - zToe); row.Z = crest; }
    const xlsxDiameter = parseNum(workbook.map.get(id));
    if (xlsxDiameter !== null) row.Diameter = xlsxDiameter;
    else { diameterFallback.push(id); row.Diameter = Math.round(number(row.Diameter, `Diameter do furo ${id}`) / INCH_IN_METERS * 10) / 10; }
    if (plannedMap) { const planned = plannedMap.get(id); if (planned > 0) { row.Stemming = planned; stemmingPlanned.push(id); } else stemmingFallback.push(id); }
    return row;
  });
  if (zMissing.length) throw new Error(`Z do CSV inválido em ${zMissing.length} furo(s) e não há XLSX com X/Y/Z Collar para corrigir. Anexe o XLSX auxiliar.`);
  const zParts = [];
  if (zFromXlsx.length) zParts.push(`obtida do XLSX em ${zFromXlsx.length} furos`);
  if (zEstimated.length) zParts.push(`estimada pelos furos vizinhos em ${zEstimated.length} (${formatRanges(zEstimated)})`);
  if (zParts.length) notices.push(`Z do CSV inválido: cota de boca ${zParts.join('; ')}.`);
  if (zDivergent.length) notices.push(`Z do CSV diferente do XLSX em mais de ${Z_TOLERANCE} m: cota do XLSX usada em ${zDivergent.length} furos (${formatRanges(zDivergent)}).`);
  if (plannedMap) notices.push(`Tampão previsto do CSV planejado aplicado em ${stemmingPlanned.length} furos${stemmingFallback.length ? `; mantido do CSV de perfuração em ${stemmingFallback.length} (${formatRanges(stemmingFallback)})` : ''}.`);
  if (diameterFallback.length) notices.push(`Diameter convertido do CSV (m para pol) em ${diameterFallback.length} furos (${formatRanges(diameterFallback)}), por ausência no XLSX.`);
  return rows;
}
generate.addEventListener('click', async () => { clearError(); generate.disabled = true; try { setProgress('Identificando os CSVs pelo conteúdo…', 10); const { drilling, planned } = await classifyCsvFiles(state.files); validateRows(drilling); setProgress('Lendo o XLSX auxiliar (opcional)…', 35); const xlsx = state.files.find(f => ['xlsx','xls'].includes(ext(f))); const workbook = xlsx ? await parseWorkbook(xlsx) : { map: new Map(), collars: new Map(), foundId: null, names: [] }; const planId = await resolveId(state.files, workbook); const planType = detectType(state.files, drilling); setProgress('Corrigindo Z, tampão e diâmetro…', 55); const notices = []; const preparedRows = prepareRows(drilling, workbook, planned ? plannedStemmingMap(planned) : null, notices); setProgress('Montando DADOS_FUROS e validando saída…', 75); const outputRows = formatOutput(buildOutput(preparedRows, planId, planType)); const headers = OUTPUT.map(([name]) => name); const sheet = XLSX.utils.json_to_sheet(outputRows, { header: headers }); sheet['!cols'] = headers.map(() => ({ wch: 15 })); applyNumberFormats(sheet, headers, outputRows.length); const outBook = XLSX.utils.book_new(); XLSX.utils.book_append_sheet(outBook, sheet, 'DADOS_FUROS'); const bytes = XLSX.write(outBook, { bookType: 'xlsx', type: 'array', compression: true }); state.output = { name: outputName(planType, planId), bytes }; setProgress('Concluído. O Excel está pronto para baixar.', 100); showResult(outputRows, planId, planType, notices); } catch (error) { fail(error.message || String(error)); } finally { generate.disabled = false; } });
$('download-button').addEventListener('click', () => { if (!state.output) return; const blob = new Blob([state.output.bytes], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }); const link = document.createElement('a'); link.href = URL.createObjectURL(blob); link.download = state.output.name; link.click(); URL.revokeObjectURL(link.href); });
function validateBundleSelection() {
  const allowed = new Set(['csv', 'xlsx', 'xls', 'pdf', 'txt']);
  const unsupported = state.files.filter(file => !allowed.has(ext(file)));
  if (unsupported.length) throw new Error(`Formato não suportado: ${unsupported.map(file => file.name).join(', ')}.`);
  const csvFiles = state.files.filter(file => ext(file) === 'csv');
  if (!csvFiles.length) throw new Error('Anexe um CSV de perfuração para continuar.');
  if (csvFiles.length > 2) throw new Error('Selecione no máximo dois CSVs: o de perfuração e, opcionalmente, o de tampão previsto.');
  const workbookFiles = state.files.filter(file => ['xlsx', 'xls'].includes(ext(file)));
  if (workbookFiles.length > 1) throw new Error('Selecione apenas um XLSX auxiliar.');
}
function typeFromText(text) { const match = String(text ?? '').match(/\b(PP|PC)\s*(?=0*\d{6,7}\b)/i); return match ? match[1].toUpperCase() : null; }
function normalizePlanName(raw) { return String(raw ?? '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toUpperCase().replace(/[^A-Z0-9]+/g, '_').replace(/^_+|_+$/g, ''); }
function planNameFromText(text) { const match = String(text ?? '').match(/Pol\S*gono\s*\/?\s*Plano\s*:?\s*(?:Data\s*:?\s*)?(.+?)(?=\s+\d{1,2}\/\d{1,2}\/\d{2,4}\b|\s+Densidade\b|\s+Desmonte\b|\s+Data\s*:|$)/i); const name = match ? match[1].trim() : ''; return /[A-Za-z]/.test(name) && name.length <= 60 && !/[:=]/.test(name) ? name : null; }
function presplitOnlyFromText(text) { const value = pattern => String(text ?? '').match(pattern)?.[1]; const isNumber = v => v !== undefined && /^\d/.test(v); return isNumber(value(/Pr\S*\s*Corte\s*=\s*(\S+)/i)) && !isNumber(value(/Produ\S*o\s*=\s*(\S+)/i)) && !isNumber(value(/Buffer\s*=\s*(\S+)/i)); }
function workbookNames(rows) { const rank = new Map([['PROJECT', 0], ['GEOMETRY', 1], ['POLIGONO', 2], ['PLANO', 2]]); const found = []; rows.forEach((row, r) => row.forEach((cell, c) => { const key = normalizePlanName(cell); if (!rank.has(key)) return; const counts = new Map(); for (const below of rows.slice(r + 1)) { const value = String(below[c] ?? '').trim(); if (/[A-Za-z]/.test(value)) counts.set(value, (counts.get(value) || 0) + 1); } const [top] = [...counts].sort((a, b) => b[1] - a[1]); if (top) found.push({ rank: rank.get(key), value: top[0] }); })); return found.sort((a, b) => a.rank - b.rank).map(item => item.value); }
function outputName(planType, planId) { return /^\d+$/.test(planId) ? `${planType}${planId}_PREV.xlsx` : `${planType}_${planId}_PREV.xlsx`; }
async function resolveId(files, workbook) {
  const ids = [], types = [], pdfNames = [], stems = [];
  let presplitOnly = false;
  for (const file of files) {
    const kind = ext(file);
    const nameId = extractId(file.name); if (nameId) ids.push(nameId);
    const nameType = typeFromText(file.name); if (nameType) types.push(nameType);
    if (['xlsx', 'xls', 'pdf'].includes(kind)) stems.push(file.name.replace(/\.[^.]+$/, ''));
    if (kind === 'pdf' || kind === 'txt') { const text = kind === 'pdf' ? await readPdfText(file) : await readText(file); const textId = extractId(text); if (textId) ids.push(textId); const textType = typeFromText(text); if (textType) types.push(textType); const label = planNameFromText(text); if (label) pdfNames.push(label); if (kind === 'pdf' && presplitOnlyFromText(text)) presplitOnly = true; }
  }
  if (workbook.foundId) ids.push(workbook.foundId);
  const uniqueIds = [...new Set(ids)], uniqueTypes = [...new Set(types)];
  if (uniqueIds.length > 1) throw new Error(`IDs de plano conflitantes encontrados: ${uniqueIds.join(', ')}.`);
  if (uniqueTypes.length > 1) throw new Error(`Tipos de plano conflitantes encontrados: ${uniqueTypes.join(', ')}.`);
  state.planType = uniqueTypes[0] || (presplitOnly ? 'PC' : null);
  if (uniqueIds.length) return uniqueIds[0];
  const planName = [...workbook.names, ...pdfNames, ...stems].map(normalizePlanName).find(Boolean);
  if (!planName) throw new Error('Não foi possível determinar o ID ou o nome do plano. Use um PDF, TXT ou XLSX com o identificador PP/PC ou com o nome do plano.');
  return planName;
}
function prepareGeneration(event) {
  $('progress-panel').hidden = false; $('result-card').hidden = true; state.output = null; state.planType = null;
  try { validateBundleSelection(); } catch (error) { event.preventDefault(); event.stopImmediatePropagation(); generate.disabled = false; fail(error.message); }
}
renderFiles();
$('generate-button').addEventListener('click', prepareGeneration, { capture: true });
input.addEventListener('change', () => { $('result-card').hidden = true; state.output = null; });
fileList.addEventListener('click', () => { $('result-card').hidden = true; state.output = null; });
