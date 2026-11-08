// Sol menü: düğme ve M tuşuyla açılıp kapanır, tercih hatırlanır. Dar alanda menü yoktur.
const KEY = "muadil.sidebar";

export function initSidebar({ button, pane, compact }) {
  let open = localStorage.getItem(KEY) !== "closed"; // varsayılan açık: menü keşfedilebilir kalsın

  const apply = () => {
    document.body.dataset.sidebar = open ? "open" : "closed";
    const label = open ? "Menüyü kapat" : "Menüyü aç";
    button.setAttribute("aria-expanded", String(open));
    button.setAttribute("aria-label", label);
    button.title = `${label} (M)`;
    pane.inert = !open && !compact.matches; // kapalıyken klavye odağı gizli satırlara gitmesin
  };

  const toggle = () => {
    if (!open && document.activeElement === document.body) button.focus({ preventScroll: true });
    if (open && pane.contains(document.activeElement)) button.focus({ preventScroll: true });
    open = !open;
    localStorage.setItem(KEY, open ? "open" : "closed");
    apply();
  };

  button.addEventListener("click", toggle);
  compact.addEventListener("change", apply);
  document.addEventListener("keydown", (e) => {
    if (e.key.toLowerCase() !== "m" || e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.target.closest?.("input, select, textarea")) return;
    if (document.body.dataset.state !== "ready" || compact.matches) return;
    toggle();
  });
  apply();
}
