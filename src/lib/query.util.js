export async function send(fetch, path, data) {

  const opts = { method: 'post', headers: {} }

  if (data) {
    opts.headers['Content-Type'] = 'application/json';
    opts.body = JSON.stringify(data);
  }
  return fetch(`${import.meta.env.VITE_APP_API}${path}`, opts)
    .then(response => response.text())
    .then(json => {
      try {
        return JSON.parse(json);
      } catch (err) {
        return json;
      }
    });
}