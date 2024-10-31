const fs = require('fs');

const files = fs.readdirSync(
  '/Users/noahbaron/Downloads/test-data/Testing/pituitary/pituitary'
);

// switch (classification.value) {
//   case 0:
//     return 'Glioma'
//   case 1:
//     return 'Meningioma'
//   case 2:
//     return 'No tumor'
//   case 3:
//     return 'Pituitary'
// }

const name = [];

files.map((file) => {
  console.log(file);
  name.push({ file, label: 3 });
});

console.log(name);
