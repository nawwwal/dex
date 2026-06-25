import { useEffect, useState } from "react";

type HeroProps = {
  title: string;
  subtitle?: string;
};

export function HeroPreview({ title, subtitle }: HeroProps) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <section className="hero">
      <h1>{title}</h1>
      {mounted ? <p>{subtitle ?? "Ready"}</p> : null}
      <img src="/product-shot.png" alt="" />
    </section>
  );
}
