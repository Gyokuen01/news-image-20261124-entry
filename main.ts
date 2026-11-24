// news-image-20261124 entry v2: copy the pre-composed front page to the
// grader's output directory, byte for byte. No network, no randomness:
// the same input file always produces the same output bytes.
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? here;
const src = join(here, "entry.png");

// Validate the pre-composed front page before copying it: it must
// exist, be non-empty, and be a PNG (or a JPEG, when compose.py fell
// back after a PNG over 1 MiB). Log its size and dimensions so a bad
// render is visible instead of silently copied.
if (!existsSync(src)) {
  console.error(`entry.png missing: ${src} (run compose.py first)`);
  process.exit(1);
}
const srcStat = statSync(src);
if (srcStat.size === 0) {
  console.error(`entry.png is empty: ${src}`);
  process.exit(1);
}
const head = readFileSync(src).subarray(0, 24);
const pngMagic = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const jpegMagic = Buffer.from([0xff, 0xd8, 0xff]);
if (head.subarray(0, 8).equals(pngMagic)) {
  // PNG IHDR: width at bytes 16-19, height at bytes 20-23, big-endian.
  const width = head.readUInt32BE(16);
  const height = head.readUInt32BE(20);
  console.log(`entry.png: PNG ${width}x${height}, ${srcStat.size} bytes`);
} else if (head.subarray(0, 3).equals(jpegMagic)) {
  console.log(`entry.png: JPEG, ${srcStat.size} bytes`);
} else {
  console.error(`entry.png is neither PNG nor JPEG: ${src}`);
  process.exit(1);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, join(outDir, "entry.png"));
const dst = join(outDir, "entry.png");
const dstStat = statSync(dst);
if (dstStat.size !== srcStat.size) {
  console.error(
    `copy mismatch: ${dst} is ${dstStat.size} bytes, expected ${srcStat.size}`,
  );
  process.exit(1);
}
console.log(`copied entry.png -> ${dst} (${dstStat.size} bytes)`);
