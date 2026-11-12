"use strict";
(() => {
  const select = document.getElementById("ghost-version");
  const button = document.getElementById("ghost-download");
  const note = document.getElementById("ghost-download-note");
  if (!select || !button || !note) return;
  const url = "/execos/ghost/x64/latest/ExecOS-x64.iso";
  const update = () => {
    const available = select.value === "x64-generic";
    button.disabled = !available;
    note.textContent = available
      ? "ExecOS Ghost x64 ISO is available, with signed automatic updates."
      : "This hardware build is not published here yet. Choose x64 generic for the available ISO.";
  };
  select.addEventListener("change", update);
  button.addEventListener("click", () => {
    if (!button.disabled && select.value === "x64-generic") window.location.assign(url);
  });
  update();
})();
