#!/usr/bin/env node
/**
 * Open-Source Image Fetcher for LinkedIn Post Skill
 *
 * Fetches images from free, open-source platforms:
 *   - Unsplash (https://unsplash.com) — requires UNSPLASH_ACCESS_KEY
 *   - Pexels (https://pexels.com) — requires PEXELS_API_KEY
 *   - Pixabay (https://pixabay.com) — requires PIXABAY_API_KEY
 *
 * Falls back through providers in order: Unsplash → Pexels → Pixabay
 *
 * Usage:
 *   node fetch_image.js --query "professional woman office" --output ./assets/photo.jpg
 *   node fetch_image.js --query "dentist clinic" --output ./assets/photo.jpg --provider pexels
 *   node fetch_image.js --query "tech startup" --output ./assets/photo.jpg --orientation portrait --size large
 */

const https = require("https");
const fs = require("fs");
const path = require("path");

// ---- API endpoints ----
const UNSPLASH_API = "https://api.unsplash.com";
const PEXELS_API = "https://api.pexels.com/v1";
const PIXABAY_API = "https://pixabay.com/api";

function parseArgs() {
  const args = process.argv.slice(2);
  const parsed = {
    query: null,
    output: null,
    provider: null, // auto-detect if not set
    orientation: null, // portrait, landscape, squarish
    size: "large", // small, medium, large
    count: 1,
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case "--query":
        parsed.query = args[++i];
        break;
      case "--output":
        parsed.output = args[++i];
        break;
      case "--provider":
        parsed.provider = args[++i];
        break;
      case "--orientation":
        parsed.orientation = args[++i];
        break;
      case "--size":
        parsed.size = args[++i];
        break;
      case "--count":
        parsed.count = parseInt(args[++i], 10);
        break;
    }
  }

  if (!parsed.query) {
    console.error("Error: --query is required");
    process.exit(1);
  }
  if (!parsed.output) {
    console.error("Error: --output is required");
    process.exit(1);
  }

  return parsed;
}

function getEnvKey(name) {
  let key = process.env[name];
  if (key) return key;

  // Try .env files
  const envPaths = [".env", "../.env", "../../.env", path.join(process.env.HOME || "", "Desktop/Prompt-OS/.env")];
  for (const envPath of envPaths) {
    try {
      if (fs.existsSync(envPath)) {
        const content = fs.readFileSync(envPath, "utf-8");
        for (const line of content.split("\n")) {
          const trimmed = line.trim();
          if (trimmed.startsWith(`${name}=`)) {
            return trimmed.split("=").slice(1).join("=").trim().replace(/^["']|["']$/g, "");
          }
        }
      }
    } catch {}
  }
  return null;
}

function httpsGet(url, headers = {}) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const options = {
      hostname: urlObj.hostname,
      path: urlObj.pathname + urlObj.search,
      headers: { ...headers, "User-Agent": "LinkedInPostSkill/1.0" },
    };

    https.get(options, (res) => {
      // Handle redirects
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        return httpsGet(res.headers.location, headers).then(resolve, reject);
      }

      if (res.statusCode !== 200) {
        let body = "";
        res.on("data", (chunk) => (body += chunk));
        res.on("end", () => reject(new Error(`HTTP ${res.statusCode}: ${body}`)));
        return;
      }

      const chunks = [];
      res.on("data", (chunk) => chunks.push(chunk));
      res.on("end", () => resolve(Buffer.concat(chunks)));
      res.on("error", reject);
    }).on("error", reject);
  });
}

async function downloadFile(url, outputPath) {
  const data = await httpsGet(url);
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, data);
  return data.length;
}

// ---- Unsplash ----
async function searchUnsplash(query, orientation, count) {
  const key = getEnvKey("UNSPLASH_ACCESS_KEY");
  if (!key) return null;

  let url = `${UNSPLASH_API}/search/photos?query=${encodeURIComponent(query)}&per_page=${count}`;
  if (orientation) url += `&orientation=${orientation}`;

  try {
    const data = await httpsGet(url, { Authorization: `Client-ID ${key}` });
    const result = JSON.parse(data.toString());
    if (!result.results || result.results.length === 0) return null;

    return result.results.map((photo) => ({
      provider: "unsplash",
      id: photo.id,
      description: photo.description || photo.alt_description || query,
      urls: {
        small: photo.urls.small,
        regular: photo.urls.regular,
        full: photo.urls.full,
      },
      photographer: photo.user.name,
      photographerUrl: photo.user.links.html,
      downloadUrl: photo.links.download_location,
      attribution: `Photo by ${photo.user.name} on Unsplash`,
    }));
  } catch (err) {
    console.error(`Unsplash error: ${err.message}`);
    return null;
  }
}

// ---- Pexels ----
async function searchPexels(query, orientation, count) {
  const key = getEnvKey("PEXELS_API_KEY");
  if (!key) return null;

  let url = `${PEXELS_API}/search?query=${encodeURIComponent(query)}&per_page=${count}`;
  if (orientation) url += `&orientation=${orientation}`;

  try {
    const data = await httpsGet(url, { Authorization: key });
    const result = JSON.parse(data.toString());
    if (!result.photos || result.photos.length === 0) return null;

    return result.photos.map((photo) => ({
      provider: "pexels",
      id: photo.id,
      description: photo.alt || query,
      urls: {
        small: photo.src.medium,
        regular: photo.src.large,
        full: photo.src.original,
      },
      photographer: photo.photographer,
      photographerUrl: photo.photographer_url,
      downloadUrl: photo.src.original,
      attribution: `Photo by ${photo.photographer} on Pexels`,
    }));
  } catch (err) {
    console.error(`Pexels error: ${err.message}`);
    return null;
  }
}

// ---- Pixabay ----
async function searchPixabay(query, orientation, count) {
  const key = getEnvKey("PIXABAY_API_KEY");
  if (!key) return null;

  // Map orientation
  let orientParam = "";
  if (orientation === "portrait") orientParam = "&orientation=vertical";
  else if (orientation === "landscape") orientParam = "&orientation=horizontal";

  const url = `${PIXABAY_API}/?key=${key}&q=${encodeURIComponent(query)}&per_page=${count}&image_type=photo&safesearch=true${orientParam}`;

  try {
    const data = await httpsGet(url);
    const result = JSON.parse(data.toString());
    if (!result.hits || result.hits.length === 0) return null;

    return result.hits.map((photo) => ({
      provider: "pixabay",
      id: photo.id,
      description: photo.tags || query,
      urls: {
        small: photo.webformatURL,
        regular: photo.largeImageURL,
        full: photo.largeImageURL,
      },
      photographer: photo.user,
      photographerUrl: `https://pixabay.com/users/${photo.user}-${photo.user_id}/`,
      downloadUrl: photo.largeImageURL,
      attribution: `Image by ${photo.user} on Pixabay`,
    }));
  } catch (err) {
    console.error(`Pixabay error: ${err.message}`);
    return null;
  }
}

async function main() {
  const args = parseArgs();

  const sizeMap = {
    small: "small",
    medium: "regular",
    large: "full",
  };
  const urlKey = sizeMap[args.size] || "regular";

  const providers = args.provider
    ? [args.provider]
    : ["unsplash", "pexels", "pixabay"];

  const searchFns = {
    unsplash: searchUnsplash,
    pexels: searchPexels,
    pixabay: searchPixabay,
  };

  let results = null;

  for (const provider of providers) {
    const fn = searchFns[provider];
    if (!fn) {
      console.error(`Unknown provider: ${provider}`);
      continue;
    }

    console.log(`Searching ${provider} for: "${args.query}"...`);
    results = await fn(args.query, args.orientation, args.count);
    if (results && results.length > 0) {
      console.log(`Found ${results.length} result(s) on ${provider}`);
      break;
    }
    console.log(`No results on ${provider}, trying next...`);
  }

  if (!results || results.length === 0) {
    console.error("Error: No images found on any provider.");
    console.error("Ensure at least one API key is set: UNSPLASH_ACCESS_KEY, PEXELS_API_KEY, or PIXABAY_API_KEY");
    process.exit(1);
  }

  // Download the first result (or multiple if count > 1)
  for (let i = 0; i < Math.min(results.length, args.count); i++) {
    const photo = results[i];
    const downloadUrl = photo.urls[urlKey] || photo.urls.regular;

    let outputPath;
    if (args.count === 1) {
      outputPath = path.resolve(args.output);
    } else {
      const ext = path.extname(args.output) || ".jpg";
      const base = path.basename(args.output, ext);
      const dir = path.dirname(args.output);
      outputPath = path.resolve(dir, `${base}_${i + 1}${ext}`);
    }

    console.log(`Downloading from ${photo.provider}: ${photo.description}`);
    const size = await downloadFile(downloadUrl, outputPath);
    console.log(`Saved: ${outputPath} (${(size / 1024).toFixed(1)} KB)`);
    console.log(`Attribution: ${photo.attribution}`);

    // Write attribution file alongside the image
    const attrPath = outputPath.replace(/\.[^.]+$/, "_attribution.txt");
    fs.writeFileSync(attrPath, `${photo.attribution}\nSource: ${photo.provider}\nID: ${photo.id}\nPhotographer URL: ${photo.photographerUrl}\n`);
  }

  // Output JSON summary to stdout for programmatic use
  const summary = results.slice(0, args.count).map((r) => ({
    provider: r.provider,
    id: r.id,
    description: r.description,
    attribution: r.attribution,
  }));
  console.log(`\n---JSON_SUMMARY---`);
  console.log(JSON.stringify(summary, null, 2));
}

main().catch((err) => {
  console.error(`Error: ${err.message}`);
  process.exit(1);
});
