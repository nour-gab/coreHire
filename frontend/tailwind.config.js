/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        core: {
          ink: "#30253E",
          teal: "#80B9B1",
          moss: "#C3C88C",
          cloud: "#F8F8F4",
          line: "#D7DFD1",
        },
      },
      borderRadius: {
        card: "10px",
      },
      boxShadow: {
        card: "0 8px 24px rgba(48, 37, 62, 0.12)",
        cardHover: "0 16px 32px rgba(48, 37, 62, 0.2)",
      },
      fontFamily: {
        display: ["Space Grotesk", "sans-serif"],
        body: ["Manrope", "sans-serif"],
      },
      animation: {
        drift: "drift 12s linear infinite",
        rise: "rise 800ms ease forwards",
      },
      keyframes: {
        drift: {
          "0%": { transform: "translateX(-20%)" },
          "100%": { transform: "translateX(20%)" },
        },
        rise: {
          "0%": { opacity: 0, transform: "translateY(18px)" },
          "100%": { opacity: 1, transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
};
