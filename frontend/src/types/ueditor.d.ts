declare namespace UE {
  interface EditorOptions {
    UEDITOR_HOME_URL?: string
    serverUrl?: string
    initialFrameWidth?: number | string
    initialFrameHeight?: number | string
    autoHeightEnabled?: boolean
    autoFloatEnabled?: boolean
    wordCount?: boolean
    maximumWords?: number
    toolbars?: any[][]
    initialContent?: string
    autoSaveEnabled?: boolean
    [key: string]: any
  }

  interface Editor {
    ready(callback: () => void): void
    setContent(content: string, isAppendTo?: boolean): void
    getContent(): string
    getContentTxt(): string
    getPlainTxt(): string
    getAllHtml(): string
    hasContents(): boolean
    destroy(): void
    addListener(type: string, callback: () => void): void
    removeListener(type: string, callback: () => void): void
    execCommand(cmd: string, value?: any): any
    focus(): void
    blur(): void
    isFocus(): boolean
    setHide(): void
    setShow(): void
    setHeight(height: number): void
    setDisabled(except?: string[]): void
    setEnabled(): void
    selection: {
      getRange(): any
      getText(): string
    }
  }

  function getEditor(id: string, options?: EditorOptions): Editor
  function delEditor(id: string): void

  namespace dom {
    namespace domUtils {
      function preventDefault(e: Event): void
      function getElementsByTagName(element: Element, tagName: string): HTMLCollectionOf<HTMLElement>
      function removeAttributes(element: Element, attrs: string[]): void
    }
  }
}

declare global {
  interface Window {
    UE: typeof UE
  }
}

export {}
