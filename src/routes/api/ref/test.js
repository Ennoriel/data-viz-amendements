export async function get() {
  // return new Promise(resolve => {
  //   setTimeout(() => resolve({
  //     body: {
  //       res: 42
  //     }
  //   }), 3000);
  // });
  return {
    body: {
      res: 42
    }
  }
  // }, 3000)
}