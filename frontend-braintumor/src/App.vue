<script setup lang="ts">
import { useTemplateRef, ref, computed } from 'vue'
import { config } from './config'
import TestImage from './components/TestImage.vue'
import { RANDOM_IMAGES, type Images } from './constants'

const inputRef = useTemplateRef('file-input')
const classification = ref<null | 0 | 1 | 2 | 3>(null)
const uploadedImageUrl = ref<null | string>(null)

const handleChange = async (event: Event) => {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return

  if (inputRef.value) inputRef.value.value = ''

  uploadedImageUrl.value = URL.createObjectURL(file)

  const formData = new FormData()
  formData.append('image', file)

  try {
    const endpoint = `${config.backendURL}/brain-tumor/predict`

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

const images = ref<Images | null>(null)

const getImages = () => {
  const imagesValues = RANDOM_IMAGES.sort(() => Math.random() - 0.5).slice(
    0,
    12,
  )
  images.value = imagesValues
}

getImages()
</script>

<template>
  <div class="header-section flex py-24 flex-col items-start px-6">
    <div class="flex flex-col gap-4 mx-auto">
      <h1
        class="text-left text-4xl md:text-5xl !leading-tight sm:text-center md:max-w-[800px]"
      >
        Detect & Classify Brain Tumors From an MRI Using AI with 79.25%
        Accuracy*
      </h1>
      <p class="text-left text-lg text-[#4D4D4D] sm:text-center">
        Trained on the
        <a
          href="https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset"
          class="underline"
          target="_blank"
          >Brain Tumor MRI Dataset</a
        >
      </p>
    </div>
    <div class="flex gap-2 flex-col mt-6 mx-auto" v-if="label !== null">
      <img
        v-if="uploadedImageUrl !== null"
        :src="uploadedImageUrl"
        alt="Uploaded MRI Image"
        class="h-80 w-auto rounded object-cover"
      />
      <p class="mx-auto text-xl text-black font-semibold">
        Prediction: {{ label }}
      </p>
    </div>
    <input
      type="file"
      accept="image/*"
      className="text-white invisible absolute -z-10 -top-full -left-full"
      @change="handleChange"
      ref="file-input"
    />
    <button
      @click="uploadImage"
      class="button w-full sm:w-56 md:w-80 sm:mx-auto rounded-full mt-5 bg-gray-900 text-white h-12"
    >
      Upload image
    </button>
    <p
      class="sm:text-center mx-auto mt-4 max-w-[500px] text-left text-[#4D4D4D]"
    >
      This is for educational purposes only and should not be used as a
      substitute for professional medical care
    </p>
  </div>
  <div class="flex flex-col pt-10 pb-4 px-7 mb-0">
    <div class="flex flex-col gap-4">
      <h1 class="text-3xl text-left sm:text-center sm:text-4xl">
        Test a random image
      </h1>
      <p class="text-left sm:text-center max-w-[600px] sm:mx-auto">
        Click a scan below to test the model. These images have never been seen
        by the model and are randomized. The AI model predicts the
        classification correctly on 79.25% of images.
      </p>
    </div>
    <button
      class="button w-56 rounded-full mt-5 bg-gray-900 text-white h-12 sm:mx-auto"
      @click="getImages"
    >
      Randomize Images
    </button>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-2 mt-8">
      <TestImage
        v-for="image in images"
        :correct-class="image.label"
        :file="image.file"
        :key="image.file"
      />
    </div>
    <div class="mt-6 mb-2 flex flex-col gap-3">
      <p class="text-gray-600">
        *accuracy calculated using 300 images not seen during training
      </p>
      <div>
        <div class="flex justify-between">
          <a
            href="https://github.com/nbaron1/detect-cancer"
            class="cursor-pointer"
            target="_blank"
          >
            <svg
              width="32"
              height="32"
              viewBox="0 0 32 32"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M16 2C8.265 2 2 8.265 2 16C2 22.195 6.0075 27.4275 11.5725 29.2825C12.2725 29.405 12.535 28.985 12.535 28.6175C12.535 28.285 12.5175 27.1825 12.5175 26.01C9 26.6575 8.09 25.1525 7.81 24.365C7.6525 23.9625 6.97 22.72 6.375 22.3875C5.885 22.125 5.185 21.4775 6.3575 21.46C7.46 21.4425 8.2475 22.475 8.51 22.895C9.77 25.0125 11.7825 24.4175 12.5875 24.05C12.71 23.14 13.0775 22.5275 13.48 22.1775C10.365 21.8275 7.11 20.62 7.11 15.265C7.11 13.7425 7.6525 12.4825 8.545 11.5025C8.405 11.1525 7.915 9.7175 8.685 7.7925C8.685 7.7925 9.8575 7.425 12.535 9.2275C13.655 8.9125 14.845 8.755 16.035 8.755C17.225 8.755 18.415 8.9125 19.535 9.2275C22.2125 7.4075 23.385 7.7925 23.385 7.7925C24.155 9.7175 23.665 11.1525 23.525 11.5025C24.4175 12.4825 24.96 13.725 24.96 15.265C24.96 20.6375 21.6875 21.8275 18.5725 22.1775C19.08 22.615 19.5175 23.455 19.5175 24.7675C19.5175 26.64 19.5 28.145 19.5 28.6175C19.5 28.985 19.7625 29.4225 20.4625 29.2825C23.2418 28.3443 25.6568 26.5581 27.3677 24.1753C29.0786 21.7926 29.9993 18.9334 30 16C30 8.265 23.735 2 16 2Z"
                fill="black"
              />
            </svg>
          </a>
          <p>
            built by
            <a
              class="text-gray-800 underline cursor-pointer"
              href="https://nbaron.com/"
              target="_blank"
              >nbaron</a
            >
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.header-section {
  background: radial-gradient(
    50.08% 50.08% at 50% 49.92%,
    #f1f1f1 0%,
    #efefef 100%
  );
}

.button {
  background: linear-gradient(90deg, #3c3a3a 0%, #504e4e 52.5%, #3c3a3a 100%);
}
</style>
