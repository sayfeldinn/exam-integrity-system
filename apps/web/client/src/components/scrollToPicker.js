// Smoothly brings the "Choose your interface" section to the middle of the screen.
export default function scrollToPicker(smooth = true) {
  document.getElementById('interfaces')?.scrollIntoView({
    behavior: smooth ? 'smooth' : 'auto',
    block: 'center',
  });
}
