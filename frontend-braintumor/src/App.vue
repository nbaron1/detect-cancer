<script setup lang="ts">
import { useTemplateRef, ref, computed } from 'vue'
import { config } from './config'

const inputRef = useTemplateRef('file-input')

const classification = ref<null | 0 | 1 | 2 | 3>(null)

// const CLASS_MAPPING = {
//   0: 'Glioma',
//   1: 'Meningioma',
//   2: 'No Tumor',
//   3: 'Pituitary',
// } as const

const handleChange = async (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return

  if (inputRef.value) inputRef.value.value = ''

  const formData = new FormData()
  formData.append('image', file)

  try {
    const endpoint = `${config.backendURL}/predict/brain-tumor`

    const response = await fetch(endpoint, {
      method: 'POST',
      body: formData,
    })

    const data = await response.json()

    classification.value = data.classification
  } catch (error) {
    console.error(error)
  } finally {
  }
}

const uploadImage = () => {
  inputRef.value?.click()
}

const label = computed(() => {
  if (classification.value === null) return null

  switch (classification.value) {
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
})
</script>

<template>
  <h1 class="text-center">
    Detect Brain Tumors from Using AI with 70% Accuracy*
  </h1>
  <p class="text-center">
    Trained on the
    <a
      href="https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset"
      class="underline"
      >Brain Tumor MRI Dataset</a
    >
  </p>
  <p v-if="label !== null">{{ label }}</p>
  <input
    type="file"
    accept="image/*"
    className="text-white invisible absolute -z-10 -top-full -left-full"
    @change="handleChange"
    ref="file-input"
  />
  <button @click="uploadImage">Upload image</button>
</template>

<style scoped></style>
