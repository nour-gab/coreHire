export default function Card({ title, subtitle, children }) {
  return (
    <section className="rounded-card border border-core-line bg-white/90 p-5 shadow-card transition duration-300 ease-in-out hover:-translate-y-1 hover:scale-[1.01] hover:shadow-cardHover">
      {title ? <h3 className="font-display text-lg text-core-ink">{title}</h3> : null}
      {subtitle ? <p className="mt-1 text-sm text-core-ink/70">{subtitle}</p> : null}
      <div className="mt-3">{children}</div>
    </section>
  );
}
