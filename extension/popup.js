const statusEl = document.getElementById("status");
const companyEl = document.getElementById("company");
const roleEl = document.getElementById("role");

function setStatus(msg) {
  statusEl.textContent = msg;
}

async function getActiveTab() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  return tab;
}

async function extractFromPage(mode) {
  const tab = await getActiveTab();

  // Inject a small function into the page to extract text
  const [{ result }] = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: (mode) => {
      const selection = window.getSelection ? window.getSelection().toString() : "";
      if (mode === "selected") {
        return selection && selection.trim().length > 0 ? selection.trim() : "";
      }

      // whole page text fallback
      const bodyText = document.body ? document.body.innerText : "";
      return bodyText ? bodyText.trim() : "";
    },
    args: [mode],
  });

  return result || "";
}

async function sendToBackend(jdText) {
  const payload = {
    company: companyEl.value || "Company",
    role: roleEl.value || "Role",
    job_description: jdText
  };

  const resp = await fetch("http://127.0.0.1:8000/tailor", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`Backend error (${resp.status}): ${text}`);
  }
  return await resp.json();
}

async function extractSmartJD() {
  const tab = await getActiveTab();

  const [{ result }] = await chrome.scripting.executeScript({
    target: { tabId: tab.id },
    func: () => {
      // Common selectors across job boards (best-effort)
      const selectors = [
        "div[data-job-description]",        // generic
        "[class*='jobDescription']",        // common naming
        "[id*='jobDescription']",
        "[class*='description']",
        "[id*='description']",
        "section[class*='description']",
        "main",
        "article"
      ];

      // Try to find the largest "dense text" container
      const candidates = [];
      for (const sel of selectors) {
        document.querySelectorAll(sel).forEach(el => {
          const text = (el.innerText || "").trim();
          // filter tiny blocks
          if (text.length > 800) candidates.push({ el, textLen: text.length, text });
        });
      }

      // If we found candidates, pick the longest
      if (candidates.length > 0) {
        candidates.sort((a, b) => b.textLen - a.textLen);
        return candidates[0].text;
      }

      // Fallback: whole page
      return (document.body?.innerText || "").trim();
    },
  });

  return result || "";
}


document.getElementById("captureSelected").addEventListener("click", async () => {
  try {
    setStatus("Extracting selected text...");
    const jd = await extractFromPage("selected");

    if (!jd || jd.length < 200) {
      setStatus("Selected text is empty/too short.\nHighlight the JD on the page first, then try again.");
      return;
    }

    setStatus("Sending JD to backend...");
    const out = await sendToBackend(jd);

    setStatus(`✅ Done!\nSaved TXT: ${out.saved_txt_to}\nSaved DOCX: ${out.saved_docx_to}`);
  } catch (e) {
    setStatus(`❌ ${e.message}`);
  }
});

document.getElementById("capturePage").addEventListener("click", async () => {
  try {
    setStatus("Extracting whole page text...");
    const jd = await extractFromPage("page");

    if (!jd || jd.length < 500) {
      setStatus("Whole page text seems too short. Try selecting the JD section instead.");
      return;
    }

    setStatus("Sending JD to backend...");
    const out = await sendToBackend(jd);

    setStatus(`✅ Done!\nSaved TXT: ${out.saved_txt_to}\nSaved DOCX: ${out.saved_docx_to}`);
  } catch (e) {
    setStatus(`❌ ${e.message}`);
  }
});

document.getElementById("captureSmart").addEventListener("click", async () => {
  try {
    setStatus("Extracting JD section (smart)...");
    const jd = await extractSmartJD();

    if (!jd || jd.length < 500) {
      setStatus("Smart capture got too little text. Try Whole Page Text.");
      return;
    }

    setStatus("Sending JD to backend...");
    const out = await sendToBackend(jd);

    setStatus(`✅ Done!\nSaved TXT: ${out.saved_txt_to}\nSaved DOCX: ${out.saved_docx_to}`);
  } catch (e) {
    setStatus(`❌ ${e.message}`);
  }
});
