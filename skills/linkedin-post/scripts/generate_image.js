#!/usr/bin/env node
/**
 * Puppeteer-based LinkedIn Post Image Generator
 *
 * Renders HTML templates into pixel-perfect LinkedIn post images.
 * Uses Puppeteer to capture high-quality screenshots of styled HTML,
 * producing professional social media graphics without any paid AI API.
 *
 * Usage:
 *   node generate_image.js --html template.html --output ./output/post.png
 *   node generate_image.js --html template.html --output ./output/post.png --width 1080 --height 1350
 *   node generate_image.js --html-string "<html>...</html>" --output ./output/post.png
 */

const puppeteer = require("puppeteer");
const path = require("path");
const fs = require("fs");

// LinkedIn dimension presets
const PRESETS = {
  portrait: { width: 1080, height: 1350 },
  square: { width: 1080, height: 1080 },
  landscape: { width: 1350, height: 1080 },
  story: { width: 1080, height: 1920 },
};

function parseArgs() {
  const args = process.argv.slice(2);
  const parsed = {
    html: null,
    htmlString: null,
    output: null,
    width: null,
    height: null,
    aspect: "portrait",
    deviceScaleFactor: 2, // Retina quality
    data: null, // JSON data for template interpolation
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case "--html":
        parsed.html = args[++i];
        break;
      case "--html-string":
        parsed.htmlString = args[++i];
        break;
      case "--output":
        parsed.output = args[++i];
        break;
      case "--width":
        parsed.width = parseInt(args[++i], 10);
        break;
      case "--height":
        parsed.height = parseInt(args[++i], 10);
        break;
      case "--aspect":
        parsed.aspect = args[++i];
        break;
      case "--scale":
        parsed.deviceScaleFactor = parseFloat(args[++i]);
        break;
      case "--data":
        parsed.data = args[++i];
        break;
    }
  }

  if (!parsed.output) {
    console.error("Error: --output is required");
    process.exit(1);
  }
  if (!parsed.html && !parsed.htmlString) {
    console.error("Error: --html or --html-string is required");
    process.exit(1);
  }

  return parsed;
}

function resolveTemplate(htmlPath, dataJson) {
  let html = fs.readFileSync(htmlPath, "utf-8");

  // If data JSON provided, do template interpolation
  if (dataJson) {
    let data;
    if (fs.existsSync(dataJson)) {
      data = JSON.parse(fs.readFileSync(dataJson, "utf-8"));
    } else {
      data = JSON.parse(dataJson);
    }

    // Replace {{key}} placeholders with data values
    for (const [key, value] of Object.entries(data)) {
      const regex = new RegExp(`\\{\\{\\s*${key}\\s*\\}\\}`, "g");
      html = html.replace(regex, value);
    }
  }

  return html;
}

async function generateImage(options) {
  const {
    html,
    htmlString,
    output,
    width,
    height,
    aspect,
    deviceScaleFactor,
    data,
  } = options;

  // Resolve dimensions
  const preset = PRESETS[aspect] || PRESETS.portrait;
  const finalWidth = width || preset.width;
  const finalHeight = height || preset.height;

  // Get HTML content
  let htmlContent;
  if (htmlString) {
    htmlContent = htmlString;
  } else {
    const htmlPath = path.resolve(html);
    if (!fs.existsSync(htmlPath)) {
      console.error(`Error: HTML file not found: ${htmlPath}`);
      process.exit(1);
    }
    htmlContent = resolveTemplate(htmlPath, data);
  }

  // Ensure output directory exists
  const outputPath = path.resolve(output);
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });

  console.log(`Generating image...`);
  console.log(`  Dimensions: ${finalWidth}x${finalHeight} (@${deviceScaleFactor}x)`);
  console.log(`  Output: ${outputPath}`);

  // Launch Puppeteer
  const browser = await puppeteer.launch({
    headless: "new",
    args: [
      "--no-sandbox",
      "--disable-setuid-sandbox",
      "--disable-dev-shm-usage",
      "--font-render-hinting=none",
    ],
  });

  try {
    const page = await browser.newPage();

    // Set viewport to exact LinkedIn dimensions
    await page.setViewport({
      width: finalWidth,
      height: finalHeight,
      deviceScaleFactor,
    });

    // Load HTML content
    await page.setContent(htmlContent, {
      waitUntil: ["networkidle0", "domcontentloaded"],
      timeout: 30000,
    });

    // Wait for fonts and images to load
    await page.evaluate(() => {
      return Promise.all([
        document.fonts ? document.fonts.ready : Promise.resolve(),
        new Promise((resolve) => {
          const images = document.querySelectorAll("img");
          if (images.length === 0) return resolve();
          let loaded = 0;
          images.forEach((img) => {
            if (img.complete) {
              loaded++;
              if (loaded === images.length) resolve();
            } else {
              img.onload = img.onerror = () => {
                loaded++;
                if (loaded === images.length) resolve();
              };
            }
          });
          // Timeout fallback for images
          setTimeout(resolve, 10000);
        }),
      ]);
    });

    // Small delay for rendering
    await new Promise((r) => setTimeout(r, 500));

    // Take screenshot
    await page.screenshot({
      path: outputPath,
      type: "png",
      clip: {
        x: 0,
        y: 0,
        width: finalWidth,
        height: finalHeight,
      },
    });

    const stats = fs.statSync(outputPath);
    console.log(`Image saved to: ${outputPath}`);
    console.log(`  Size: ${(stats.size / 1024).toFixed(1)} KB`);
    console.log(`  Effective resolution: ${finalWidth * deviceScaleFactor}x${finalHeight * deviceScaleFactor}px`);
  } finally {
    await browser.close();
  }
}

// Main
const args = parseArgs();
generateImage(args).catch((err) => {
  console.error(`Error generating image: ${err.message}`);
  process.exit(1);
});
