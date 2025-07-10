import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar.jsx'
import { 
  Search, 
  Home, 
  Clock, 
  User, 
  Star, 
  MapPin, 
  Wrench, 
  Zap, 
  Hammer, 
  Paintbrush,
  Droplets,
  Scissors,
  ArrowLeft,
  Phone,
  MessageCircle
} from 'lucide-react'
import './App.css'

function App() {
  const [currentView, setCurrentView] = useState('home')
  const [selectedCategory, setSelectedCategory] = useState('')
  const [selectedProfessional, setSelectedProfessional] = useState(null)
  const [categories, setCategories] = useState([])
  const [professionals, setProfessionals] = useState([])
  const [reviews, setReviews] = useState([])
  const [loading, setLoading] = useState(false)

  const iconMap = {
    'zap': Zap,
    'droplets': Droplets,
    'hammer': Hammer,
    'paintbrush': Paintbrush,
    'wrench': Wrench,
    'scissors': Scissors
  }

  const colorMap = {
    'electricista': 'bg-yellow-100 text-yellow-800',
    'plomero': 'bg-blue-100 text-blue-800',
    'carpintero': 'bg-amber-100 text-amber-800',
    'pintor': 'bg-purple-100 text-purple-800',
    'mecanico': 'bg-gray-100 text-gray-800',
    'peluquero': 'bg-pink-100 text-pink-800'
  }

  // Fetch categories on component mount
  useEffect(() => {
    fetchCategories()
    fetchFeaturedProfessionals()
  }, [])

  const fetchCategories = async () => {
    try {
      const response = await fetch('/api/categories')
      const data = await response.json()
      setCategories(data)
    } catch (error) {
      console.error('Error fetching categories:', error)
    }
  }

  const fetchFeaturedProfessionals = async () => {
    try {
      const response = await fetch('/api/professionals')
      const data = await response.json()
      setProfessionals(data.slice(0, 2)) // Show only first 2 for featured
    } catch (error) {
      console.error('Error fetching featured professionals:', error)
    }
  }

  const fetchProfessionalsByCategory = async (category) => {
    setLoading(true)
    try {
      const response = await fetch(`/api/professionals?category=${category}`)
      const data = await response.json()
      setProfessionals(data)
    } catch (error) {
      console.error('Error fetching professionals:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchProfessionalReviews = async (professionalId) => {
    try {
      const response = await fetch(`/api/professionals/${professionalId}/reviews`)
      const data = await response.json()
      setReviews(data)
    } catch (error) {
      console.error('Error fetching reviews:', error)
    }
  }

  const handleCategorySelect = (categoryId) => {
    setSelectedCategory(categoryId)
    setCurrentView('professionals')
    fetchProfessionalsByCategory(categoryId)
  }

  const handleProfessionalSelect = (professional) => {
    setSelectedProfessional(professional)
    setCurrentView('profile')
    fetchProfessionalReviews(professional.id)
  }

  const handleBack = () => {
    if (currentView === 'profile') {
      setCurrentView('professionals')
    } else if (currentView === 'professionals') {
      setCurrentView('home')
      fetchFeaturedProfessionals() // Refresh featured professionals
    }
  }

  const renderStars = (rating) => {
    return Array.from({ length: 5 }, (_, i) => (
      <Star
        key={i}
        className={`w-4 h-4 ${
          i < Math.floor(rating) ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'
        }`}
      />
    ))
  }

  const renderHome = () => (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm p-4">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <Input
            placeholder="Buscar servicios o profesionales"
            className="pl-10 py-3 text-lg"
          />
        </div>
      </div>

      {/* Categories */}
      <div className="p-4">
        <h2 className="text-xl font-semibold mb-4 text-gray-800">Categorías de Servicios</h2>
        <div className="grid grid-cols-2 gap-4">
          {categories.map((category) => {
            const IconComponent = iconMap[category.icon] || Wrench
            const colorClass = colorMap[category.id] || 'bg-gray-100 text-gray-800'
            return (
              <Card
                key={category.id}
                className="cursor-pointer hover:shadow-md transition-shadow"
                onClick={() => handleCategorySelect(category.id)}
              >
                <CardContent className="p-6 text-center">
                  <div className={`w-16 h-16 rounded-full ${colorClass} flex items-center justify-center mx-auto mb-3`}>
                    <IconComponent className="w-8 h-8" />
                  </div>
                  <h3 className="font-medium text-gray-800">{category.name}</h3>
                </CardContent>
              </Card>
            )
          })}
        </div>
      </div>

      {/* Featured Services */}
      <div className="p-4">
        <h2 className="text-xl font-semibold mb-4 text-gray-800">Servicios Destacados</h2>
        <div className="space-y-3">
          {professionals.map((prof) => (
            <Card key={prof.id} className="cursor-pointer hover:shadow-md transition-shadow">
              <CardContent className="p-4">
                <div className="flex items-center space-x-3">
                  <Avatar>
                    <AvatarFallback>{prof.avatar}</AvatarFallback>
                  </Avatar>
                  <div className="flex-1">
                    <h3 className="font-medium">{prof.name}</h3>
                    <div className="flex items-center space-x-1">
                      {renderStars(prof.rating)}
                      <span className="text-sm text-gray-600">({prof.reviews_count})</span>
                    </div>
                    <p className="text-sm text-gray-600">{prof.specialties.join(', ')}</p>
                  </div>
                  <Badge variant={prof.available ? 'default' : 'secondary'}>
                    {prof.available ? 'Disponible' : 'Ocupado'}
                  </Badge>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Bottom Navigation */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-4 py-2">
        <div className="flex justify-around">
          <Button variant="ghost" className="flex flex-col items-center space-y-1 text-blue-600">
            <Home className="w-6 h-6" />
            <span className="text-xs">Inicio</span>
          </Button>
          <Button variant="ghost" className="flex flex-col items-center space-y-1 text-gray-600">
            <Clock className="w-6 h-6" />
            <span className="text-xs">Historial</span>
          </Button>
          <Button variant="ghost" className="flex flex-col items-center space-y-1 text-gray-600">
            <User className="w-6 h-6" />
            <span className="text-xs">Perfil</span>
          </Button>
        </div>
      </div>
    </div>
  )

  const renderProfessionals = () => {
    const categoryName = categories.find(c => c.id === selectedCategory)?.name || 'Profesionales'

    return (
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-white shadow-sm p-4">
          <div className="flex items-center space-x-3">
            <Button variant="ghost" size="sm" onClick={handleBack}>
              <ArrowLeft className="w-5 h-5" />
            </Button>
            <h1 className="text-xl font-semibold">{categoryName}</h1>
          </div>
          <div className="flex items-center mt-3 text-sm text-gray-600">
            <MapPin className="w-4 h-4 mr-1" />
            <span>Santa Fe</span>
          </div>
        </div>

        {/* Professionals List */}
        <div className="p-4 space-y-4">
          {loading ? (
            <div className="text-center py-8">
              <p className="text-gray-600">Cargando profesionales...</p>
            </div>
          ) : (
            professionals.map((prof) => (
              <Card
                key={prof.id}
                className="cursor-pointer hover:shadow-md transition-shadow"
                onClick={() => handleProfessionalSelect(prof)}
              >
                <CardContent className="p-4">
                  <div className="flex items-center space-x-4">
                    <Avatar className="w-16 h-16">
                      <AvatarFallback className="text-lg">{prof.avatar}</AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                      <h3 className="text-lg font-medium">{prof.name}</h3>
                      <div className="flex items-center space-x-1 mb-1">
                        {renderStars(prof.rating)}
                        <span className="text-sm text-gray-600">({prof.reviews_count})</span>
                      </div>
                      <p className="text-sm text-gray-600 mb-1">A {prof.distance}</p>
                      <p className="text-sm text-gray-600">{prof.specialties.join(', ')}</p>
                    </div>
                    <div className="text-right">
                      <Badge variant={prof.available ? 'default' : 'secondary'} className="mb-2">
                        {prof.available ? 'Disponible' : 'Ocupado'}
                      </Badge>
                      <p className="text-sm font-medium">{prof.price}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>

        {/* Bottom Navigation */}
        <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-4 py-2">
          <div className="flex justify-around">
            <Button variant="ghost" className="flex flex-col items-center space-y-1 text-gray-600">
              <Home className="w-6 h-6" />
              <span className="text-xs">Inicio</span>
            </Button>
            <Button variant="ghost" className="flex flex-col items-center space-y-1 text-blue-600">
              <Clock className="w-6 h-6" />
              <span className="text-xs">Historial</span>
            </Button>
            <Button variant="ghost" className="flex flex-col items-center space-y-1 text-gray-600">
              <User className="w-6 h-6" />
              <span className="text-xs">Perfil</span>
            </Button>
          </div>
        </div>
      </div>
    )
  }

  const renderProfile = () => {
    if (!selectedProfessional) return null

    return (
      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <div className="bg-white shadow-sm p-4">
          <div className="flex items-center justify-between">
            <Button variant="ghost" size="sm" onClick={handleBack}>
              <ArrowLeft className="w-5 h-5" />
            </Button>
            <h1 className="text-xl font-semibold">Perfil</h1>
            <div className="w-8"></div>
          </div>
        </div>

        {/* Profile Content */}
        <div className="p-4 space-y-6">
          {/* Profile Header */}
          <Card>
            <CardContent className="p-6 text-center">
              <Avatar className="w-24 h-24 mx-auto mb-4">
                <AvatarFallback className="text-2xl">{selectedProfessional.avatar}</AvatarFallback>
              </Avatar>
              <h2 className="text-2xl font-bold mb-2">{selectedProfessional.name}</h2>
              <div className="flex items-center justify-center space-x-1 mb-2">
                {renderStars(selectedProfessional.rating)}
                <span className="text-sm text-gray-600">({selectedProfessional.reviews_count})</span>
              </div>
              <div className="flex items-center justify-center text-gray-600 mb-4">
                <MapPin className="w-4 h-4 mr-1" />
                <span>A {selectedProfessional.distance}</span>
              </div>
              <Badge variant={selectedProfessional.available ? 'default' : 'secondary'}>
                {selectedProfessional.available ? 'Disponible' : 'Ocupado'}
              </Badge>
              {selectedProfessional.description && (
                <p className="text-sm text-gray-600 mt-4">{selectedProfessional.description}</p>
              )}
            </CardContent>
          </Card>

          {/* Services */}
          <Card>
            <CardHeader>
              <CardTitle>Servicios</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {selectedProfessional.specialties.map((specialty, index) => (
                  <div key={index} className="flex justify-between items-center">
                    <span>{specialty}</span>
                    <span className="font-medium">{selectedProfessional.price}</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Tarifas */}
          <Card>
            <CardHeader>
              <CardTitle>Tarifas</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex justify-between items-center">
                <span>Visita:</span>
                <span className="font-medium text-lg">{selectedProfessional.price}</span>
              </div>
            </CardContent>
          </Card>

          {/* Opiniones */}
          <Card>
            <CardHeader>
              <CardTitle>Opiniones</CardTitle>
              <CardDescription>{selectedProfessional.reviews_count} reseñas</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {reviews.map((review) => (
                  <div key={review.id} className="border-b pb-4 last:border-b-0">
                    <div className="flex items-center space-x-2 mb-2">
                      <Avatar className="w-8 h-8">
                        <AvatarFallback>{review.client_avatar}</AvatarFallback>
                      </Avatar>
                      <div>
                        <p className="font-medium text-sm">{review.client_name}</p>
                        <div className="flex items-center">
                          {renderStars(review.rating)}
                        </div>
                      </div>
                    </div>
                    <p className="text-sm text-gray-600">{review.comment}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Action Buttons */}
        <div className="fixed bottom-20 left-0 right-0 p-4 bg-white border-t">
          <div className="flex space-x-3">
            <Button variant="outline" className="flex-1">
              <Phone className="w-4 h-4 mr-2" />
              Llamar
            </Button>
            <Button variant="outline" className="flex-1">
              <MessageCircle className="w-4 h-4 mr-2" />
              Mensaje
            </Button>
          </div>
          <Button className="w-full mt-3 bg-blue-600 hover:bg-blue-700">
            Solicitar Trabajo
          </Button>
        </div>

        {/* Bottom Navigation */}
        <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-4 py-2">
          <div className="flex justify-around">
            <Button variant="ghost" className="flex flex-col items-center space-y-1 text-gray-600">
              <Home className="w-6 h-6" />
              <span className="text-xs">Inicio</span>
            </Button>
            <Button variant="ghost" className="flex flex-col items-center space-y-1 text-gray-600">
              <Clock className="w-6 h-6" />
              <span className="text-xs">Historial</span>
            </Button>
            <Button variant="ghost" className="flex flex-col items-center space-y-1 text-gray-600">
              <User className="w-6 h-6" />
              <span className="text-xs">Perfil</span>
            </Button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-md mx-auto bg-white">
      {currentView === 'home' && renderHome()}
      {currentView === 'professionals' && renderProfessionals()}
      {currentView === 'profile' && renderProfile()}
    </div>
  )
}

export default App

