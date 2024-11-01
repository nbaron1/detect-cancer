export const getLabelFromClass = (classType: number) => {
  switch (classType) {
    case 0:
      return 'Glioma'
    case 1:
      return 'Meningioma'
    case 2:
      return 'No tumor'
    case 3:
      return 'Pituitary'
  }

  return null
}
