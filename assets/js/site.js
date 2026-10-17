(() => {
  const burger = document.getElementById("burger");
  const header = document.querySelector(".site-header");

  if (burger) {
    burger.addEventListener("click", () => {
      const open = document.body.classList.toggle("nav-open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
      burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
  }

  if (header && document.body.classList.contains("home")) {
    const sync = () => header.classList.toggle("is-solid", window.scrollY > 24);
    sync();
    window.addEventListener("scroll", sync, { passive: true });
  }

  const form = document.getElementById("contact-form");
  if (form) {
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const name = (form.elements.namedItem("name")?.value || "").trim();
      const email = (form.elements.namedItem("email")?.value || "").trim();
      const topic = (form.elements.namedItem("topic")?.value || "").trim();
      const message = (form.elements.namedItem("body")?.value || "").trim();
      const subject = encodeURIComponent(`ZITO enquiry — ${topic}`);
      const body = encodeURIComponent(
        `Name: ${name}\nEmail: ${email}\nTopic: ${topic}\n\n${message}`
      );
      window.location.href = `mailto:hello@zitoglobal.com?subject=${subject}&body=${body}`;
    });
  }

  const nodes = document.querySelectorAll(".reveal");
  if (!nodes.length) return;

  if (!("IntersectionObserver" in window)) {
    nodes.forEach((el) => el.classList.add("is-in"));
    return;
  }

  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -5% 0px" }
  );

  nodes.forEach((el) => io.observe(el));
})();
