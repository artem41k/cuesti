export const copyFormLink = async (id) => {
  await navigator.clipboard.writeText(`${window.location.origin}/f/${id}`);
}

export const getCurrentMode = () => {
  const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  return prefersDark ? 'dark' : 'light';
}

export const darkenHslColor = (hslString) => {
  const newLightness = getCurrentMode() === 'dark' ? 50 : 70;
  return hslString.slice(0, hslString.length-4) + `${newLightness}%)`;
}

export const darkenHexColor = (hex, amount = 20) => {
  let col = hex.startsWith('#') ? hex.slice(1) : hex;
  if (col.length === 3) col = col.split('').map(c => c + c).join('');
  const num = parseInt(col, 16);
  const r = Math.max((num >> 16) - amount, 0);
  const g = Math.max((num >> 8 & 0x00FF) - amount, 0);
  const b = Math.max((num & 0x0000FF) - amount, 0);
  return `#${(r << 16 | g << 8 | b).toString(16).padStart(6, '0')}`;
}

export const shuffleArray = (array) => {
  const shuffled = [...array];
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
  }
  return shuffled;
}