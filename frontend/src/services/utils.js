export const copyFormLink = async (id) => {
  await navigator.clipboard.writeText(`${window.location.origin}/f/${id}`);
}