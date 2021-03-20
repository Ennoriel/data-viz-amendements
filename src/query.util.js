export async function send(path, data) {

  const opts = {
    method: 'post',
    headers: {}
  }

  if(data) {
    opts.headers['Content-Type']='application/json';
    opts.body=JSON.stringify(data);
  }

  return fetch(path, opts)
    .then(response => response.text())
    .then(json => {
      try {
        return JSON.parse(json);
      } catch(err) {
        return json;
      }
    });
}