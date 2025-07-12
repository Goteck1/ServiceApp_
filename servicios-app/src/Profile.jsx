import { useUser } from './UserContext.jsx'

function Profile() {
  const { user } = useUser()

  if (!user) {
    return <div className="p-4">No hay usuario autenticado.</div>
  }

  return (
    <div className="p-4 space-y-2">
      <h1 className="text-xl font-semibold">Perfil</h1>
      <p>Usuario: {user.username}</p>
      <p>Email: {user.email}</p>
    </div>
  )
}

export default Profile
