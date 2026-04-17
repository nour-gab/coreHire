import { useMemo } from "react";

export default function AnimatedHeroLines() {
  const lines = useMemo(
    () =>
      Array.from({ length: 16 }, (_, idx) => ({
        id: idx,
        top: `${idx * 7}%`,
        delay: `${idx * 0.2}s`,
      })),
    [],
  );

  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden">
      {lines.map((line) => (
        <div
          key={line.id}
          className="absolute h-px w-[140%] -left-[20%] animate-drift bg-gradient-to-r from-transparent via-core-teal/35 to-transparent"
          style={{ top: line.top, animationDelay: line.delay }}
        />
      ))}
      <div className="absolute -top-32 right-10 h-72 w-72 rounded-full bg-core-moss/40 blur-3xl" />
      <div className="absolute bottom-0 left-0 h-80 w-80 rounded-full bg-core-teal/30 blur-3xl" />
    </div>
  );
}
