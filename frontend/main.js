// Fetch the visitor count from the Azure Function and show it in the footer.
// The API is added in a later step; until then the page keeps showing "-".
async function loadCount() {
  const el = document.getElementById("count");
  try {
    const res = await fetch("/api/counter");
    if (!res.ok) throw new Error("HTTP " + res.status);
    const data = await res.json();
    el.textContent = data.count;
  } catch (err) {
    console.log("Counter unavailable:", err);
  }
}

loadCount();
