// Radar geometrisi: eksen izdüşümü ve iki profilin örtüştüğü alanın sınırı.

// i. eksen saat yönünde, tepeden başlar; v 0–1
export function projector(cx, cy, radius, axes) {
  return (i, v) => {
    const angle = (2 * Math.PI * i) / axes;
    return [cx + radius * v * Math.sin(angle), cy - radius * v * Math.cos(angle)];
  };
}

export const toPoints = (points) => points.map(([x, y]) => `${x.toFixed(1)},${y.toFixed(1)}`).join(" ");

function intersection([ax, ay], [bx, by], [cx, cy], [dx, dy]) {
  const rx = bx - ax, ry = by - ay, sx = dx - cx, sy = dy - cy;
  const t = ((cx - ax) * sy - (cy - ay) * sx) / (rx * sy - ry * sx);
  return [ax + t * rx, ay + t * ry];
}

// Her eksende küçük olan değer; iki çizginin kesiştiği yerde kesişim noktası eklenir.
export function sharedOutline(a, b, project) {
  const axes = a.length;
  const outline = [];
  for (let i = 0; i < axes; i++) {
    const j = (i + 1) % axes;
    outline.push(project(i, Math.min(a[i], b[i])));
    if ((a[i] - b[i]) * (a[j] - b[j]) < 0) {
      outline.push(intersection(project(i, a[i]), project(j, a[j]), project(i, b[i]), project(j, b[j])));
    }
  }
  return outline;
}
