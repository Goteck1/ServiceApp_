/* global process */
import { useState } from 'react'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Button } from '@/components/ui/button.jsx'
import { useUser } from './UserContext.jsx'

function LoginTabs({ onSuccess }) {
  const { setUser } = useUser()
  const API_URL = process.env.REACT_APP_API_URL || '/api'

  const [loginData, setLoginData] = useState({ username: '', password: '' })
  const [registerData, setRegisterData] = useState({ username: '', email: '', password: '' })

  const handleChange = (setter) => (e) => {
    setter((prev) => ({ ...prev, [e.target.name]: e.target.value }))
  }

  const handleLogin = async (e) => {
    e.preventDefault()
    const res = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(loginData)
    })
    if (res.ok) {
      const data = await res.json()
      setUser(data.user)
      onSuccess && onSuccess()
    }
  }

  const handleRegister = async (e) => {
    e.preventDefault()
    const res = await fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(registerData)
    })
    if (res.ok) {
      const data = await res.json()
      setUser(data.user)
      onSuccess && onSuccess()
    }
  }

  return (
    <Tabs defaultValue="login" className="p-4 space-y-4">
      <TabsList className="grid w-full grid-cols-2">
        <TabsTrigger value="login">Iniciar sesión</TabsTrigger>
        <TabsTrigger value="register">Registrarse</TabsTrigger>
      </TabsList>
      <TabsContent value="login">
        <form onSubmit={handleLogin} className="space-y-3 mt-4">
          <Input name="username" placeholder="Usuario" value={loginData.username} onChange={handleChange(setLoginData)} />
          <Input type="password" name="password" placeholder="Contraseña" value={loginData.password} onChange={handleChange(setLoginData)} />
          <Button type="submit" className="w-full">Entrar</Button>
        </form>
      </TabsContent>
      <TabsContent value="register">
        <form onSubmit={handleRegister} className="space-y-3 mt-4">
          <Input name="username" placeholder="Usuario" value={registerData.username} onChange={handleChange(setRegisterData)} />
          <Input name="email" type="email" placeholder="Email" value={registerData.email} onChange={handleChange(setRegisterData)} />
          <Input type="password" name="password" placeholder="Contraseña" value={registerData.password} onChange={handleChange(setRegisterData)} />
          <Button type="submit" className="w-full">Crear cuenta</Button>
        </form>
      </TabsContent>
    </Tabs>
  )
}

export default LoginTabs
