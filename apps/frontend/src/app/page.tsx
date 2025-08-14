"use client";

import { useEffect, useRef, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";
type Item = { id:number; title:string|null; url:string };

export default function Home() {
  const [items, setItems] = useState<Item[]>([]);
  const fileRef = useRef<HTMLInputElement>(null);

  async function refresh() {
    const r = await fetch(`${API}/images`);
    setItems(await r.json());
  }
  useEffect(() => { refresh(); }, []);

  async function upload(files: FileList | null) {
    if (!files || files.length === 0) return;
    const fd = new FormData();
    Array.from(files).forEach(f => fd.append("files", f));
    const r = await fetch(`${API}/upload`, { method: "POST", body: fd });
    if (r.ok) await refresh();
  }

  // drag-and-drop upload onto the + tile
  function handleDrop(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
    upload(e.dataTransfer.files);
  }
  function handleDragOver(e: React.DragEvent<HTMLDivElement>) {
    e.preventDefault();
  }

  async function remove(id:number) {
    await fetch(`${API}/images/${id}`, { method: "DELETE" });
    await refresh();
  }

  async function annotate(id:number) {
    const text = prompt("Text to write on image:");
    if (!text) return;
    const fd = new FormData();
    fd.append("image_id", String(id));
    fd.append("text", text);
    const r = await fetch(`${API}/annotate`, { method: "POST", body: fd });
    if (r.ok) await refresh();
  }

  return (
    <main className="min-h-screen">
      {/* NavBar */}
      <nav className="sticky top-0 z-10 bg-white/80 backdrop-blur border-b">
        <div className="mx-auto max-w-6xl px-4 py-3 flex items-center justify-between">
          <h1 className="text-lg font-semibold">Hyperfotopixelicious</h1>

          <div className="flex items-center gap-3">
            {/* Add (navbar button mirrors the + tile) */}
            <button
              onClick={() => fileRef.current?.click()}
              className="inline-flex items-center gap-2 rounded-xl border px-3 py-2"
              title="Pick multiple WhatsApp images to import"
            >
              Import from WhatsApp
            </button>
            <button onClick={refresh} className="rounded-xl border px-3 py-2">
              Refresh
            </button>
          </div>
        </div>
      </nav>

      {/* Hidden picker (also used by + tile) */}
      <input
        ref={fileRef}
        type="file"
        multiple
        accept="image/*"
        onChange={(e)=> upload(e.target.files)}
        className="hidden"
      />

      {/* Grid = images + one permanent + tile */}
      <section className="mx-auto max-w-6xl px-4 py-6 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
        {/* existing images */}
        {items.map(it => (
          <article key={it.id} className="group border rounded-2xl overflow-hidden">
            <img src={it.url} alt={it.title ?? "image"} className="w-full aspect-square object-cover" />
            <div className="p-2 flex gap-3">
              <button onClick={()=>annotate(it.id)} className="text-sm underline">Add text</button>
              <button onClick={()=>remove(it.id)} className="text-sm text-red-600 underline">Delete</button>
            </div>
          </article>
        ))}

        {/* + tile (drop or click to add) */}
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onClick={() => fileRef.current?.click()}
          title="Drop images here or click to pick"
          className="cursor-pointer rounded-2xl border-2 border-dashed flex items-center justify-center aspect-square bg-white hover:bg-gray-50"
        >
          <div className="w-20 h-20 rounded-3xl border relative">
            <span className="absolute inset-0 before:absolute before:inset-x-1/2 before:-translate-x-1/2 before:top-3 before:bottom-3 before:w-[3px] before:bg-black
                               after:absolute after:inset-y-1/2 after:-translate-y-1/2 after:left-3 after:right-3 after:h-[3px] after:bg-black"></span>
          </div>
        </div>
      </section>
    </main>
  );
}
