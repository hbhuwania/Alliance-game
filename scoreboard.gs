/************************************************************************
 * Alliance HQ — Shared Leaderboard backend (Google Apps Script)
 * ---------------------------------------------------------------------
 * This tiny free script gives the game a leaderboard that syncs across
 * EVERYONE's phones (not just one device). No servers, no cost.
 *
 * SETUP (about 5 minutes, one time):
 *  1. Go to https://sheets.google.com and create a new blank spreadsheet.
 *  2. In the menu: Extensions -> Apps Script.
 *  3. Delete whatever code is there, paste THIS whole file, and Save.
 *  4. Click Deploy -> New deployment -> (gear) Web app.
 *       - Description: Alliance HQ leaderboard
 *       - Execute as: Me
 *       - Who has access: Anyone
 *     Click Deploy, allow the permissions it asks for.
 *  5. Copy the "Web app URL" it gives you (ends with /exec).
 *  6. Open index.html, find the line:  const SHARED_ENDPOINT = "";
 *     and paste your URL between the quotes. Save. Done!
 *
 * Everyone who opens the game link now shares one live leaderboard,
 * reset automatically each week (scores are stored per week).
 ************************************************************************/

const SHEET_NAME = 'scores';

function getSheet_() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sh = ss.getSheetByName(SHEET_NAME);
  if (!sh) {
    sh = ss.insertSheet(SHEET_NAME);
    sh.appendRow(['week', 'name', 'score', 'diff', 'timestamp']);
  }
  return sh;
}

// GET  /exec?week=2026-W31   ->  [{name, score, diff}, ...] (best per player)
function doGet(e) {
  const week = (e && e.parameter && e.parameter.week) || '';
  const sh = getSheet_();
  const rows = sh.getDataRange().getValues();
  const best = {};
  for (let i = 1; i < rows.length; i++) {
    const [w, name, score] = rows[i];
    if (week && String(w) !== week) continue;
    const key = String(name).toLowerCase();
    const s = Number(score) || 0;
    if (!best[key] || s > best[key].score) best[key] = { name: String(name), score: s };
  }
  const out = Object.values(best).sort((a, b) => b.score - a.score).slice(0, 50);
  return ContentService
    .createTextOutput(JSON.stringify(out))
    .setMimeType(ContentService.MimeType.JSON);
}

// POST body: {"week":"2026-W31","name":"Bhaiya","score":1234,"diff":"superfan"}
function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents);
    const week = String(body.week || '').slice(0, 12);
    const name = String(body.name || 'Player').slice(0, 24);
    const score = Math.max(0, Math.min(100000, Number(body.score) || 0));
    const diff = String(body.diff || 'casual').slice(0, 12);
    if (week && name) {
      getSheet_().appendRow([week, name, score, diff, new Date()]);
    }
    return ContentService
      .createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
