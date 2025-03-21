// Get URL Parameter
const params = new URLSearchParams(window.location.search);
const url = params.get("url") || "example.com"; // Default value
document.getElementById("scannedUrl").innerText = url;

// Simulated Trust Score (Replace with AI API later)
const trustScore = Math.floor(Math.random() * 100);

// Update UI
document.getElementById("scoreDisplay").innerText = trustScore + "%";
const needle = document.getElementById("needle");
needle.style.transform = `rotate(${(trustScore / 100) * 180 - 90}deg)`;

// Define Factors
const factors = [
    { name: "IP Address in URL", description: "Detects if a raw IP is used instead of a domain.", risk: 10 },
    { name: "URL Length", description: "Longer URLs can be suspicious.", risk: 8 },
    { name: "Shortening Services", description: "Checks for bit.ly, tinyurl, etc.", risk: 7 },
    { name: "Having '@' Symbol", description: "Phishing URLs sometimes use @ to mask the real site.", risk: 5 },
    { name: "Double Slash Redirect", description: "Some phishing sites use // to redirect.", risk: 6 },
    { name: "Prefix/Suffix in Domain", description: "Checks if '-' is used in the domain.", risk: 6 },
    { name: "Subdomain Count", description: "More subdomains can be risky.", risk: 9 },
    { name: "SSL Certificate Validity", description: "Phishing sites often lack SSL.", risk: 12 },
    { name: "Domain Registration Length", description: "Shorter registration times can indicate scams.", risk: 7 },
    { name: "Favicon Check", description: "Scammers may use favicons from trusted sites.", risk: 6 },
    { name: "Unusual Ports", description: "Some scams use non-standard ports.", risk: 5 },
    { name: "HTTPS Token in Domain", description: "Phishing sites may include 'https' in the name.", risk: 8 },
    { name: "Request URL Ratio", description: "Measures external object requests.", risk: 7 },
    { name: "Anchor Tag Ratio", description: "Checks if <a> tags point externally.", risk: 7 },
    { name: "Links in Tags Ratio", description: "Measures suspicious <meta> links.", risk: 6 },
    { name: "SFH (Server Form Handler)", description: "Detects fake login forms.", risk: 9 },
    { name: "Submitting to Email", description: "Phishing forms often submit to emails.", risk: 6 },
    { name: "Abnormal URL", description: "Checks if URL structure is unusual.", risk: 7 },
    { name: "Redirects Count", description: "Too many redirects indicate phishing.", risk: 5 },
    { name: "Mouseover Behavior", description: "Scammers hide real URLs on hover.", risk: 4 },
    { name: "Right Click Disabled", description: "Some phishing sites block right-click.", risk: 5 },
    { name: "Pop-Up Windows", description: "Scam sites often use pop-ups.", risk: 6 },
    { name: "Iframe Usage", description: "Hidden iframes are a phishing trick.", risk: 7 },
    { name: "Domain Age", description: "New domains are more likely scams.", risk: 10 },
    { name: "DNS Record Availability", description: "Missing DNS records indicate risk.", risk: 9 },
    { name: "Web Traffic Rank", description: "Phishing sites have little traffic.", risk: 8 },
    { name: "Page Rank Score", description: "Google ranking of the site.", risk: 7 },
    { name: "Google Indexing", description: "Checks if Google indexes the site.", risk: 6 },
    { name: "Statistical Report Flag", description: "If flagged in security databases.", risk: 9 }
];

// Display Factors
const analysisList = document.getElementById("analysisList");
factors.forEach(factor => {
    const factorDiv = document.createElement("div");
    factorDiv.innerHTML = `<b>${factor.name}</b>: ${factor.description}`;
    
    if (factor.risk > 8) factorDiv.classList.add("dangerous");
    else if (factor.risk > 5) factorDiv.classList.add("suspicious");
    else factorDiv.classList.add("safe");

    analysisList.appendChild(factorDiv);
});
