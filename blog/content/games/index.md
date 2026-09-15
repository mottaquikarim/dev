---
title: "Word Games"
description: "Daily word games by Taq Karim — Freestyle, Ditty, Wordle Time Machine, Fall and Whodoku."
date: 2026-09-15T00:00:00Z
---

<style>
.games-list { margin: 2em 0; }
.game-card {
  display: flex; align-items: center; gap: 18px;
  padding: 16px 8px; border-bottom: 1px solid #e8e8e8;
  text-decoration: none !important;
}
.games-list .game-card:first-child { border-top: 1px solid #e8e8e8; }
.game-card:hover { background: #fafafa; }
.game-card img {
  width: 72px; height: 72px; border-radius: 22.5%;
  flex-shrink: 0; box-shadow: 0 1px 4px rgba(0,0,0,.12);
}
.game-card .g-body { flex: 1; min-width: 0; }
.game-card h3 { margin: 0 0 4px !important; font-size: 1.9rem; color: #313a3d; }
.game-card p { margin: 0 !important; color: #6b7280; font-size: 1.5rem; line-height: 1.4; }
.game-card .g-play { color: #007dfa; font-size: 1.5rem; white-space: nowrap; }
@media (max-width: 500px) {
  .game-card img { width: 60px; height: 60px; }
  .game-card .g-play { display: none; }
}
</style>

A collection of the daily word games I've built over the years. All free, all playable in your browser.

<div class="games-list">
  <a class="game-card" href="https://playfreestyle.co">
    <img src="/dev/games/freestyle.png" alt="Freestyle icon">
    <div class="g-body">
      <h3>Freestyle</h3>
      <p>The daily rhyming word game. Find words that rhyme with the seed — before your guesses run out.</p>
    </div>
    <span class="g-play">Play &rarr;</span>
  </a>
  <a class="game-card" href="https://taq.is/ditty/">
    <img src="/dev/games/ditty.png" alt="Ditty icon">
    <div class="g-body">
      <h3>Ditty</h3>
      <p>Wordle, but you have to rhyme. Every guess must rhyme with the last.</p>
    </div>
    <span class="g-play">Play &rarr;</span>
  </a>
  <a class="game-card" href="https://mottaquikarim.github.io/wordle_timemachine/v2.html">
    <img src="/dev/games/timemachine.png" alt="Wordle Time Machine icon">
    <div class="g-body">
      <h3>Wordle Time Machine</h3>
      <p>Play any Wordle word of the day — past or future.</p>
    </div>
    <span class="g-play">Play &rarr;</span>
  </a>
  <a class="game-card" href="https://mottaquikarim.github.io/fall/">
    <img src="/dev/games/fall.png" alt="Fall icon">
    <div class="g-body">
      <h3>Fall</h3>
      <p>A brand-new twist on a classic word game. Guess the Word of the Day before your tries run out.</p>
    </div>
    <span class="g-play">Play &rarr;</span>
  </a>
  <a class="game-card" href="https://mottaquikarim.github.io/whodoku/">
    <img src="/dev/games/whodoku.png" alt="Whodoku icon">
    <div class="g-body">
      <h3>Whodoku?</h3>
      <p>A daily celebrity sudoku. Solve the grid to reveal who the mystery person is.</p>
    </div>
    <span class="g-play">Play &rarr;</span>
  </a>
</div>
