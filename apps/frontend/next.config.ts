import type { NextConfig } from "next";
import path from "path";

const nextConfig: NextConfig = {
  distDir: path.join(process.env.HOME || "", ".next-hyperfotopixelicious"),
  /* other config options here */
};

export default nextConfig;
