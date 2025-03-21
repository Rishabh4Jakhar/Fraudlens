// Get URL Parameter
const params = new URLSearchParams(window.location.search);
const url = params.get("url") || "example.com"; // Default value
document.getElementById("scannedUrl").innerText = url;

// Simulated Trust Score (Replace with AI API later)
const trustScore = 0;

// Update UI
//document.getElementById("scoreDisplay").innerText = trustScore + "%";
//const needle = document.getElementById("needle");
//needle.style.transform = `rotate(${(trustScore / 100) * 180 - 90}deg)`;

// Define Factors
const factors = [
  {
    name: "IP Address in URL",
    description: "Detects if a raw IP is used instead of a domain.",
    risk: 10,
  },
  {
    name: "URL Length",
    description: "Longer URLs can be suspicious.",
    risk: 8,
  },
  {
    name: "Shortening Services",
    description: "Checks for bit.ly, tinyurl, etc.",
    risk: 7,
  },
  {
    name: "Having '@' Symbol",
    description: "Phishing URLs sometimes use @ to mask the real site.",
    risk: 5,
  },
  {
    name: "Double Slash Redirect",
    description: "Some phishing sites use // to redirect.",
    risk: 6,
  },
  {
    name: "Prefix/Suffix in Domain",
    description: "Checks if '-' is used in the domain.",
    risk: 6,
  },
  {
    name: "Subdomain Count",
    description: "More subdomains can be risky.",
    risk: 9,
  },
  {
    name: "SSL Certificate Validity",
    description: "Phishing sites often lack SSL.",
    risk: 12,
  },
  {
    name: "Domain Registration Length",
    description: "Shorter registration times can indicate scams.",
    risk: 7,
  },
  {
    name: "Favicon Check",
    description: "Scammers may use favicons from trusted sites.",
    risk: 6,
  },
  {
    name: "Unusual Ports",
    description: "Some scams use non-standard ports.",
    risk: 5,
  },
  {
    name: "HTTPS Token in Domain",
    description: "Phishing sites may include 'https' in the name.",
    risk: 8,
  },
  {
    name: "Request URL Ratio",
    description: "Measures external object requests.",
    risk: 7,
  },
  {
    name: "Anchor Tag Ratio",
    description: "Checks if <a> tags point externally.",
    risk: 7,
  },
  {
    name: "Links in Tags Ratio",
    description: "Measures suspicious <meta> links.",
    risk: 6,
  },
  {
    name: "SFH (Server Form Handler)",
    description: "Detects fake login forms.",
    risk: 9,
  },
  {
    name: "Submitting to Email",
    description: "Phishing forms often submit to emails.",
    risk: 6,
  },
  {
    name: "Abnormal URL",
    description: "Checks if URL structure is unusual.",
    risk: 7,
  },
  {
    name: "Redirects Count",
    description: "Too many redirects indicate phishing.",
    risk: 5,
  },
  {
    name: "Mouseover Behavior",
    description: "Scammers hide real URLs on hover.",
    risk: 4,
  },
  {
    name: "Right Click Disabled",
    description: "Some phishing sites block right-click.",
    risk: 5,
  },
  {
    name: "Pop-Up Windows",
    description: "Scam sites often use pop-ups.",
    risk: 6,
  },
  {
    name: "Iframe Usage",
    description: "Hidden iframes are a phishing trick.",
    risk: 7,
  },
  {
    name: "Domain Age",
    description: "New domains are more likely scams.",
    risk: 10,
  },
  {
    name: "DNS Record Availability",
    description: "Missing DNS records indicate risk.",
    risk: 9,
  },
  {
    name: "Web Traffic Rank",
    description: "Phishing sites have little traffic.",
    risk: 8,
  },
  {
    name: "Page Rank Score",
    description: "Google ranking of the site.",
    risk: 7,
  },
  {
    name: "Google Indexing",
    description: "Checks if Google indexes the site.",
    risk: 6,
  },
  {
    name: "Statistical Report Flag",
    description: "If flagged in security databases.",
    risk: 9,
  },
];

// Display Factors
const analysisList = document.getElementById("analysisList");
factors.forEach((factor) => {
  const factorDiv = document.createElement("div");
  factorDiv.innerHTML = `<b>${factor.name}</b>: ${factor.description}`;

  if (factor.risk > 8) factorDiv.classList.add("dangerous");
  else if (factor.risk > 5) factorDiv.classList.add("suspicious");
  else factorDiv.classList.add("safe");

  analysisList.appendChild(factorDiv);
});

document.addEventListener("DOMContentLoaded", function () {
  const scanButton = document.querySelector(".scan__form button");
  const urlInput = document.querySelector(".scan__form input");
  const trustScoreSpan = document.getElementById("trustscore");
  const scoreDisplay = document.getElementById("scoreDisplay");
  const scannedUrlSpan = document.getElementById("scannedUrl");
  const analysisList = document.getElementById("analysisList");
  const pieChart = document.getElementById("pieChart");
  const trustScoreText = document.getElementById("trustScoreText");

  function isValidURL(url) {
      return /^(https?:\/\/)?([\w\-]+(\.[\w\-]+)+)(:\d+)?(\/.*)?$/i.test(url);
  }

  function formatURL(url) {
      return url.startsWith("http://") || url.startsWith("https://") ? url : "http://" + url;
  }

  scanButton.addEventListener("click", async function () {
      let websiteURL = formatURL(urlInput.value.trim());

      if (!isValidURL(websiteURL)) {
          alert("❌ Please enter a valid URL.");
          return;
      }

      console.log(`🔍 Scanning URL: ${websiteURL}`);
      scannedUrlSpan.textContent = websiteURL;

      try {
          let response = await fetch("/api/check-website/", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ url: websiteURL }),
          });

          if (!response.ok) throw new Error("Failed to fetch API data");

          let data = await response.json();
          console.log("✅ API Response:", data);

          let trustScore = data.trust_score || 0;
          let riskLevel = data.risk_level || "Unknown Risk";
          let actionRequired = data.action || "No action needed.";

          trustScoreSpan.textContent = `${trustScore}%`;
          //scoreDisplay.textContent = `${trustScore} / 100`;
          trustScoreText.textContent = `${trustScore}%`; // Update center text

          analysisList.innerHTML = `
              <li><strong>Risk Level:</strong> ${riskLevel}</li><br>
              <li><strong>Action Required:</strong> ${actionRequired}</li>
          `;

          // Update the pie chart using CSS conic-gradient
          pieChart.style.background = `conic-gradient(#2ecc71 ${trustScore}%, #e74c3c 0%)`;

      } catch (error) {
          console.error("❌ Error fetching website scan results:", error);
          alert("⚠️ Error fetching website scan results. Please try again.");
      }
  });

  urlInput.addEventListener("keypress", function (event) {
      if (event.key === "Enter") {
          scanButton.click();
      }
  });
});
