import { ref } from 'vue'

export function useConfirmChangeDialog() {
  const confirmationQuestion = ref('')
  const dialogVisible = ref(false)
  const handleConfirmation = ref(() => {})
  const selectedItem = ref()

  function openConfirmDialog(item: any, question: string, handleConfirmationFunction: any) {
    confirmationQuestion.value = question
    dialogVisible.value = true
    selectedItem.value = item
    handleConfirmation.value = handleConfirmationFunction
  }

  function updateDialogVisible(value: boolean) {
    dialogVisible.value = value
  }

  return {
    selectedItem,
    confirmationQuestion,
    dialogVisible,
    openConfirmDialog,
    handleConfirmation,
    updateDialogVisible,
  }
}
