// scripts/embed-images.js
const fs = require("fs");
const path = require("path");

// load your raw animation JSON
const animPath = path.resolve(__dirname, "../assets/animations/logo.json");
const anim = JSON.parse(fs.readFileSync(animPath, "utf8"));

// for each asset in the JSON, read its PNG and inline it
anim.assets.forEach((asset) => {
  // only inline if it's pointing at a .png
  if (asset.p && asset.p.endsWith(".png")) {
    const imgPath = path.resolve(__dirname, "../assets/animations", asset.p);
    const b64 = fs.readFileSync(imgPath).toString("base64");
    // turn it into a full data URI:
    asset.p = `data:image/png;base64,${b64}`;
    asset.u = ""; // clear any URL prefix
  }
});

// write out a new JSON with embedded images
const outPath = path.resolve(
  __dirname,
  "../assets/animations/logo-embedded.json"
);
fs.writeFileSync(outPath, JSON.stringify(anim, null, 2));
console.log("✅ Wrote", outPath);
