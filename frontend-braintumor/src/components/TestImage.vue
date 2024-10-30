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

defineProps<{
  src: string
}>()

const prediction = ref<null | string>(null)

const handleTestModel = () => {
  prediction.value = 'Not a tumor'
}
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
        class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-stone-100 px-6 py-8 rounded-xl w-[90vw] sm:max-w-[400px] shadow-sm flex flex-col gap-6"
      >
        <div class="flex justify-between items-center">
          <DialogTitle class="text-lg font-semibold sm:text-xl">
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
        <div class="flex flex-col gap-2">
          <div class="flex gap-1 items-center">
            <p class="font-medium">Label:</p>
            <p>Not a tumor</p>
          </div>
          <div class="flex gap-1 items-center">
            <p class="font-medium">Prediction:</p>
            <div
              v-if="prediction === null"
              class="bg-stone-200 w-28 h-6 animate-pulse rounded-md"
            ></div>
            <p v-if="prediction !== null">
              {{ prediction }}
            </p>
          </div>
        </div>
        <img :src="src" class="w-full aspect-square rounded-lg bg-stone-300" />
        <button
          class="button rounded-lg bg-gray-900 text-white h-12 outline-none"
          @click="handleTestModel"
        >
          Test the model
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
