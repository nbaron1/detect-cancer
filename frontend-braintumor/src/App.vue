<script setup lang="ts">
import { useTemplateRef, ref } from 'vue'
import { config } from './config'

const inputRef = useTemplateRef('file-input')

type KeyOf<T> = T extends object ? keyof T : never

const classification = ref<null | KeyOf<typeof CLASS_MAPPING>>(null)

const CLASS_MAPPING = {
  0: 'Glioma',
  1: 'Meningioma',
  2: 'No Tumor',
  3: 'Pituitary',
} as const

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
  <p v-if="classification !== null">{{ CLASS_MAPPING[classification] }}</p>
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
