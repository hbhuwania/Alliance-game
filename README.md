# 🕹️ Alliance HQ — Weekly Trivia Challenge

A fun, mobile-first trivia game for fans of **_Alliance_** (the Prime Video reality show hosted by Kunal Kemmu).
Built to be dropped into a **WhatsApp group** — one link, play on any phone, challenge each other.

> _Fan-made and not affiliated with Prime Video, Banijay Asia, or the makers of the show._

---

## ✨ What it does

- **Show-styled game** — you "enter HQ," earn **points** (the show's only currency) against a timer, and get ranked by **The System** from _Eliminated → Rookie Ally → Survivor → Ace of the Week → Master of the System_.
- **Rounds that mirror the show:**
  - ⚡ **Rapid Challenges** — faster answers = more points
  - 🎯 **Secret Mission** — bonus questions worth **double**
  - 🗡️ **The Veto** — betrayal "trap" questions, read carefully
  - 👑 **Ace of the Week** — the final, highest-value question
- **🔥 Streak bonus** for consecutive correct answers.
- **Two difficulties** — _Casual Fan_ and _Superfan_ (cast, duos, format deep-cuts).
- **📅 New quiz every week** — a fresh, randomized set unlocks automatically. Everyone playing the same week gets the **same questions**, so the leaderboard is a fair competition.
- **🎁 Daily Bonus** — one extra question every day (same for everyone, one shot). Its points add to your weekly total, so there's a reason to come back each day.
- **👑 Ace of the Week** — last week's #1 is crowned on the home screen automatically.
- **🏆 Persistent leaderboard** — every player's best score is saved and ranked. Works per-device out of the box, or **synced across the whole group** (optional, see below).
- **📲 One-tap WhatsApp share** — brag about your rank and challenge the group to beat your score.

---

## 🚀 Get a shareable link (for WhatsApp)

The game is a single file (`index.html`). Publish it free with **GitHub Pages**. You only do this once.

**Fastest way (recommended — no build needed):**
1. On GitHub, open **Settings → Pages**.
2. Under **Build and deployment → Source**, choose **Deploy from a branch**.
3. Branch: **`claude/alliance-india-game-0jdoyo`** (or `main` after you merge) · Folder: **`/ (root)`** · **Save**.
4. Wait ~1 minute, then your link is live:
   **`https://hbhuwania.github.io/Alliance-game/`**
5. Paste that link into your WhatsApp group. 🎉

**Via GitHub Actions instead:** a workflow (`.github/workflows/pages.yml`) is included and runs on the `main` branch. To use it, set **Settings → Pages → Source: GitHub Actions**, then merge to `main` (or click **Run workflow**). _Note: the first time, GitHub may need you to enable Pages in Settings once — the workflow token can't turn it on by itself._

_No GitHub Pages? You can also just open `index.html` on any phone, or host it on any static host (Netlify Drop, Vercel, etc.)._

---

## 🌐 Optional: one shared leaderboard across everyone's phones

By default each phone keeps its own leaderboard (simple, works offline). To make **one live leaderboard for the whole group**:

1. Open **`scoreboard.gs`** and follow the step-by-step setup at the top (about 5 minutes). It gives you a **Web app URL**.
2. **No code editing needed** — open the game, tap **“🌐 Group leaderboard”** on the home screen, and paste the URL. The game copies a special invite link (`…/?board=…`).
3. **Share that invite link in WhatsApp.** Anyone who taps it automatically joins the same live leaderboard, reset automatically each week.

_(Prefer hardcoding? You can instead set `const HARDCODED_ENDPOINT = "…"` near the top of `index.html`.)_

---

## 💬 Invite message for the family / WhatsApp group

Copy-paste this with your link:

> 🕹️ *Alliance HQ — Trivia Challenge!*
> Think you're the biggest *Alliance* fan in this group? 😏
> Enter HQ, beat the clock, and see if The System crowns you 👑 *Ace of the Week*.
> 🎁 New quiz every week + a daily bonus question.
> Play here 👉 `<your-link>`
> Post your rank & score — let's see who gets eliminated first 💀🔥

---

## ✏️ Editing / adding questions

Open `index.html` and find the `BANK = [ ... ]` array near the top of the `<script>`. Each question:

```js
{
  q: "Question text?",
  opts: ["Right answer", "Wrong", "Wrong", "Wrong"],
  a: 0,                 // index of the correct option in opts[]
  tier: "casual",       // "casual" (everyone) or "superfan" (close viewers)
  type: "normal",       // "normal" | "mission" (2x) | "veto" (trap) | "ace" (finale)
  ex: "Short explanation shown after answering."
}
```

Add as many as you like — the weekly picker mixes them up so the game stays fresh. Keep a healthy number of each `type` so every week has Secret Missions, Vetos, and an Ace question.

---

## 💡 Ideas to extend it

See the bottom of this README's companion notes, but quick wins: daily bonus question, a "Traitor or Ally" party mode, avatars/alliance colours per player, sound effects, and a "share the exact question you got wrong" taunt. PRs welcome from the group!

---

## 🎬 About the show (for question-writers)

- **Alliance** — Prime Video (Hindi), hosted by **Kunal Kemmu** (his reality-hosting debut).
- Based on Talpa Studios' Dutch format by **John de Mol**; produced by **Banijay Asia**.
- **16 celebrities** enter as **8 duos**, form larger **alliances of 4**, inside a bunker (**"Kunal Lok" / HQ**) run by **"The System."**
- **42 episodes / 6 weeks**, a new episode **daily at 12 noon** — Prime Video's first-ever global daily reality series. Winner takes **₹50 lakh**.
- The 8 duos: Ravi Kishan & Riva Kishan · Kushal Tandon & Arslan Goni · Daisy Shah & Zaid Darbar · Nikhil Chinapa & Mini Mathur · Payal Dhare & Sabby Suri · Niti Taylor & Ruhee Dosani · Vanshaj Singh & Dolly Javed · Delbar Arya & Armaan Khera.

Enjoy — and may The System be ever in your favour. 👑
