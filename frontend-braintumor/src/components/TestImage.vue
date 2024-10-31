<script setup lang="ts">
import {
  DialogClose,
  DialogContent,
  DialogOverlay,
  DialogPortal,
  DialogRoot,
  DialogTitle,
  DialogTrigger,
} from 'radix-vue'
import { ref } from 'vue'
import { config } from '../config'

const { file } = defineProps<{
  file: string
}>()

const prediction = ref<null | string>(null)
const confidence = ref<null | number>(null)

const predictionError = ref<boolean>()

const handleMakePrediction = async (url: string) => {
  try {
    console.log(src)

    const response = await fetch(
      `${config.backendURL}/brain-tumor/predict-url`,
      {
        method: 'POST',
        body: JSON.stringify({
          url,
        }),
        headers: {
          'Content-Type': 'application/json',
        },
      },
    )

    const data = await response.json()

    console.log({ data })

    if (!('success' in data) || !data.success) {
      throw new Error('Missing valid success message')
    }

    confidence.value = data.predictionError.value
    prediction.value = data.predictionError.classification
  } catch {
    predictionError.value = true
  }
}

const src = `https://www.brain-tumor-static.nbaron.com/${file}`
</script>

<template>
  <DialogRoot>
    <DialogTrigger
      ><img :src="src" class="aspect-square w-full bg-stone-200 rounded-xl"
    /></DialogTrigger>
    <DialogPortal>
      <DialogOverlay
        class="fixed top-0 left-0 right-0 bottom-0 bg-black opacity-20"
      />
      <DialogContent
        aria-describedby="undefined"
        class="fixed top-1/2 left-1/2 z-10 -translate-x-1/2 -translate-y-1/2 bg-stone-100 px-8 py-8 rounded-2xl w-[90vw] sm:max-w-[400px] shadow-sm flex flex-col gap-6"
      >
        <div class="flex justify-between items-center">
          <DialogTitle class="text-xl font-semibold sm:text-xl">
            Test the model
          </DialogTitle>
          <DialogClose>
            <svg
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M18 6L6 18M6 6L18 18"
                stroke="black"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </DialogClose>
        </div>
        <div class="flex flex-col gap-4">
          <div class="flex gap-1 items-center">
            <p class="font-medium">Label:</p>
            <p>Not a tumor</p>
          </div>
          <div class="flex flex-col gap-2">
            <div class="flex gap-1 items-center">
              <p class="font-medium">Prediction:</p>
              <p v-if="prediction === null" class="font-medium">
                Click "Make prediction"
              </p>
              <p v-else>
                {{ prediction }}
              </p>
            </div>
            <div class="flex gap-1 items-center">
              <p class="font-medium">Confidence:</p>
              <p v-if="confidence === null" class="font-medium">
                Click "Make prediction"
              </p>
              <p v-else>
                {{ `${(confidence * 100).toFixed(0)}%` }}
              </p>
            </div>
          </div>
        </div>
        <img :src="src" class="w-full aspect-square rounded-lg bg-stone-300" />
        <button
          class="button rounded-lg bg-gray-900 text-white h-12 outline-none"
          @click="handleMakePrediction(src)"
        >
          Make prediction
        </button>
      </DialogContent>
    </DialogPortal>
  </DialogRoot>
</template>

<style scoped>
.button {
  background: linear-gradient(90deg, #3c3a3a 0%, #504e4e 52.5%, #3c3a3a 100%);
}
</style>
