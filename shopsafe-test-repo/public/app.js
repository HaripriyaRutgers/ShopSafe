// TRAINING FIXTURE ONLY — not a functioning credential.
// Planted issue #1: public JavaScript contains an apparent secret value.
const INTERNAL_API_KEY = 'sk_test_SHOPSAFE_FAKE_1234567890';

const btn = document.getElementById('lookup');
btn.addEventListener('click', async () => {
  const order = document.getElementById('order').value;
  const viewer = document.getElementById('viewer').value;
  const out = document.getElementById('result');
  out.textContent = 'Loading...';
  try {
    const response = await fetch(`/api/order?id=${encodeURIComponent(order)}&viewer=${encodeURIComponent(viewer)}`);
    const data = await response.json();
    out.textContent = JSON.stringify({status:response.status, ...data}, null, 2);
  } catch (err) { out.textContent = 'Request failed: ' + err.message; }
});
