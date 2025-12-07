#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import sharp from "sharp";
import { createClient } from "@supabase/supabase-js";
import { readFile, unlink, writeFile } from "fs/promises";
import { resolve, dirname, basename, extname, join, sep } from "path";
import { randomUUID } from "crypto";
import { tmpdir } from "os";

// Character sets for ASCII art
const CHAR_SETS = {
  simple: " .:-=+*#%@",
  detailed: " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$",
  blocks: " ░▒▓█",
  minimal: " .-+*#@",
  matrix: " .:-=+*#@"
} as const;

type CharSetName = keyof typeof CHAR_SETS;
type ColorMode = "gray" | "color";

// Initialize Supabase client
const supabaseUrl = process.env.SUPABASE_URL || "";
const supabaseKey = process.env.SUPABASE_KEY || "";
const supabaseBucket = process.env.SUPABASE_BUCKET || "ascii-art-images";
const supabaseClient = supabaseUrl && supabaseKey 
  ? createClient(supabaseUrl, supabaseKey)
  : null;

// Create server instance
const server = new McpServer({
  name: "ascii-art",
  version: "1.0.0",
});

/**
 * Upload file to Supabase Storage
 */
async function uploadToSupabase(
  filePath: string,
  inputBasename: string
): Promise<string> {
  if (!supabaseClient) {
    throw new Error("Supabase not configured. Set SUPABASE_URL and SUPABASE_KEY environment variables.");
  }

  // Generate unique filename with UUID to avoid overwriting
  const uniqueFileName = `${inputBasename}_${randomUUID()}.png`;
  const fileBuffer = await readFile(filePath);
  
  const { data, error } = await supabaseClient.storage
    .from(supabaseBucket)
    .upload(uniqueFileName, fileBuffer, {
      contentType: 'image/png',
      cacheControl: '3600',
      upsert: false  // Don't overwrite existing files
    });
  
  if (error) {
    throw new Error(`Supabase upload failed: ${error.message}`);
  }
  
  const { data: urlData } = supabaseClient.storage
    .from(supabaseBucket)
    .getPublicUrl(uniqueFileName);
  
  return urlData.publicUrl;
}

/**
 * Create ASCII art image
 */
async function createAsciiImage(
  imagePath: string,
  outputPath: string,
  width: number,
  charset: string,
  colorMode: ColorMode
): Promise<{ width: number; height: number; size: number }> {
  const image = sharp(imagePath);
  const metadata = await image.metadata();
  
  if (!metadata.width || !metadata.height) {
    throw new Error("Unable to get image dimensions");
  }

  const aspectRatio = metadata.height / metadata.width;
  
  // Font settings (monospace)
  const fontSize = 10;
  const charWidth = fontSize * 0.6; // Monospace character width is ~0.6 of font size
  const charHeight = fontSize;

  // Calculate height to maintain aspect ratio considering character dimensions
  // We want: (height * charHeight) / (width * charWidth) = aspectRatio
  // So: height = aspectRatio * width * (charWidth / charHeight)
  const height = Math.round(aspectRatio * width * (charWidth / charHeight));

  const canvasWidth = Math.round(width * charWidth);
  const canvasHeight = height * charHeight;

  // Resize image
  const processedImage = image.resize(width, height, { fit: 'fill' });

  // Get both grayscale (for character selection) and color data
  const grayImage = processedImage.clone().grayscale();
  const { data: grayPixels } = await grayImage.raw().toBuffer({ resolveWithObject: true });
  
  let colorPixels: Uint8Array | undefined;
  if (colorMode === "color") {
    const rgbImage = processedImage.clone().toColorspace('srgb');
    const result = await rgbImage.raw().toBuffer({ resolveWithObject: true });
    colorPixels = result.data;
  }

  // Create ASCII art with colors
  interface CharData {
    char: string;
    x: number;
    y: number;
    color: string;
  }
  
  const chars: CharData[] = [];
  
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const idx = y * width + x;
      const brightness = grayPixels[idx];
      const charIndex = Math.floor((brightness / 255) * (charset.length - 1));
      const char = charset[charIndex];
      
      // Skip spaces (keep background)
      if (char === ' ') {
        continue;
      }
      
      const xPos = x * charWidth;
      const yPos = y * charHeight + charHeight; // Add charHeight for baseline
      
      let color: string;
      if (colorMode === "color" && colorPixels) {
        const colorIdx = idx * 3;
        let r = colorPixels[colorIdx];
        let g = colorPixels[colorIdx + 1];
        let b = colorPixels[colorIdx + 2];
        
        // Ensure colors are bright enough to be visible on dark background
        const minBrightness = 80;
        const totalBrightness = r + g + b;
        if (totalBrightness < minBrightness * 3) {
          const factor = (minBrightness * 3) / Math.max(totalBrightness, 1);
          r = Math.min(255, Math.round(r * factor));
          g = Math.min(255, Math.round(g * factor));
          b = Math.min(255, Math.round(b * factor));
        }
        
        color = `rgb(${r},${g},${b})`;
      } else {
        // Grayscale mode: adjust text color based on brightness
        const grayValue = Math.round(brightness * 0.7 + 76); // Map to 76-255 range
        color = `rgb(${grayValue},${grayValue},${grayValue})`;
      }
      
      chars.push({ char, x: xPos, y: yPos, color });
    }
  }

  // Helper function to escape XML special characters
  const escapeXml = (text: string): string => {
    return text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&apos;');
  };

  // Create SVG with individual colored characters
  const svgContent = `<?xml version="1.0" encoding="UTF-8"?>
<svg width="${canvasWidth}" height="${canvasHeight}" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="rgb(40,44,52)"/>
  <g font-family="Consolas,Monaco,monospace" font-size="${fontSize}">
${chars.map(({ char, x, y, color }) => 
    `    <text x="${x.toFixed(2)}" y="${y}" fill="${color}">${escapeXml(char)}</text>`
  ).join('\n')}
  </g>
</svg>`;

  // Convert SVG to PNG using sharp
  const pngBuffer = await sharp(Buffer.from(svgContent))
    .png()
    .toBuffer();

  await writeFile(outputPath, pngBuffer);
  
  const stats = await sharp(outputPath).metadata();
  
  return {
    width: stats.width || canvasWidth,
    height: stats.height || canvasHeight,
    size: pngBuffer.length
  };
}

/**
 * Validate absolute path
 */
function validateAbsolutePath(path: string): { isValid: boolean; error?: string } {
  const parsedPath = resolve(path);
  
  // Check if it's an absolute path
  // On Windows: starts with drive letter (e.g., C:\, D:\)
  // On Unix: starts with /
  const isAbsolute = /^[a-zA-Z]:\\/.test(path) || path.startsWith('/');
  
  if (!isAbsolute) {
    return {
      isValid: false,
      error: `Only absolute paths are allowed. Got relative path: ${path}\n💡 Hint: Use full path like 'D:\\folder\\image.jpg'`
    };
  }
  
  return { isValid: true };
}

// Register single consolidated generate_ascii_image tool with Supabase upload
server.tool(
  "generate_ascii_image",
  "Generate ASCII art from an image and upload to cloud storage. This tool converts an image to ASCII art, renders it as a PNG image with VS Code dark theme styling, uploads to Supabase, and returns the public URL.",
  {
    image_path: z.string().describe("ABSOLUTE path to the input image file (relative paths are not allowed)"),
    width: z.number().optional().default(100).describe("Width of ASCII art in characters (default: 100, recommended: 80-120 for images)"),
    charset: z.enum(["simple", "detailed", "blocks", "minimal", "matrix"]).optional().default("detailed").describe("Character set to use. Options: 'simple' (basic set), 'detailed' (70+ characters for detail, default), 'blocks' (Unicode blocks), 'minimal' (clean and simple), 'matrix' (Matrix style)"),
    color_mode: z.enum(["gray", "color"]).optional().default("gray").describe("Output mode: 'gray' for grayscale ASCII art (default), 'color' for colored ASCII with original image colors")
  },
  async ({ image_path, width = 100, charset = "detailed", color_mode = "gray" }) => {
    let tempFilePath: string | null = null;
    try {
      // Validate absolute path
      const pathValidation = validateAbsolutePath(image_path);
      if (!pathValidation.isValid) {
        return {
          content: [{ type: "text", text: `❌ Error: ${pathValidation.error}` }]
        };
      }

      const inputPath = resolve(image_path);
      const inputBasename = basename(inputPath, extname(inputPath));
      
      // Create temporary file path
      tempFilePath = join(tmpdir(), `ascii_${randomUUID()}_${inputBasename}.png`);

      const charSet = CHAR_SETS[charset as CharSetName];
      const result = await createAsciiImage(
        inputPath,
        tempFilePath,
        width,
        charSet,
        color_mode as ColorMode
      );

      // Upload to Supabase
      const publicUrl = await uploadToSupabase(tempFilePath, inputBasename);

      return {
        content: [{
          type: "text",
          text: `✅ ASCII art image generated and uploaded successfully!\n🌐 Public URL: ${publicUrl}\n📐 Dimensions: ${result.width}×${result.height} pixels\n💾 File size: ${(result.size / 1024).toFixed(2)} KB`
        }]
      };
    } catch (error) {
      return {
        content: [{
          type: "text",
          text: `❌ Error: ${error instanceof Error ? error.message : String(error)}`
        }]
      };
    } finally {
      // Clean up temporary file
      if (tempFilePath) {
        try {
          await unlink(tempFilePath);
        } catch {
          // Ignore cleanup errors
        }
      }
    }
  }
);

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("ASCII Art MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error in main():", error);
  process.exit(1);
});
