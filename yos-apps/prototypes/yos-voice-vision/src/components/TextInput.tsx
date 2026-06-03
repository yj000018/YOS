'use client'

import { useState, useRef, useEffect } from 'react'

interface TextInputProps {
  onSend: (text: string) => void
  disabled?: boolean
}

export default function TextInput({ onSend, disabled = false }: TextInputProps) {
  const [value, setValue] = useState('')
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    // Auto-focus when text mode activates
    if (!disabled) {
      inputRef.current?.focus()
    }
  }, [disabled])

  const handleSubmit = () => {
    const text = value.trim()
    if (!text || disabled) return
    onSend(text)
    setValue('')
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  return (
    <div className="w-full animate-fade-in">
      <div className="glass-card rounded-2xl p-1 flex items-center gap-2 border border-yos-accent/20">
        <input
          ref={inputRef}
          type="text"
          value={value}
          onChange={e => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          placeholder="Type a message…"
          className="flex-1 bg-transparent text-yos-text text-sm px-3 py-2.5 outline-none placeholder:text-yos-muted/40 disabled:opacity-40"
        />
        <button
          onClick={handleSubmit}
          disabled={disabled || !value.trim()}
          className="w-9 h-9 rounded-xl flex items-center justify-center transition-all duration-200 disabled:opacity-30"
          style={{
            background: value.trim() && !disabled
              ? 'rgba(79, 110, 247, 0.25)'
              : 'transparent',
          }}
          aria-label="Send"
        >
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path
              d="M14 8L2 2l3 6-3 6 12-6z"
              fill="currentColor"
              className={value.trim() && !disabled ? 'text-yos-accent' : 'text-yos-muted'}
            />
          </svg>
        </button>
      </div>
      <p className="text-center text-yos-muted/30 text-xs mt-1.5">
        Enter to send · conversation continues
      </p>
    </div>
  )
}
