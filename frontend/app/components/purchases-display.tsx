import { Calendar, Star } from 'lucide-react'
interface Purchase {
  item_id: string
  name: string
  description: string
  price: number
  quantity: number
  link: string
  rate: number
  image_link: string
  timestamp: string
}

const StarRating = ({ rating }: { rating: number }) => {
  return (
    <div className="flex items-center">
      {[1, 2, 3, 4, 5].map((star) => (
        <Star
          key={star}
          className={`w-4 h-4 ${
            star <= rating ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300'
          }`}
        />
      ))}
    </div>
  )
}

const PurchaseCard = ({ purchase }: { purchase: Purchase }) =>{
    const purchaseDate = new Date(purchase.time_stamp)

    return (
  <div className="bg-white rounded-lg shadow-md overflow-hidden transition-all duration-300 hover:shadow-lg hover:scale-105">
    <div className="p-6">
      <h2 className="text-xl font-bold mb-2 text-gray-800">{purchase.name}</h2>
      <img src={purchase.image_link} alt={purchase.name} className="w-full h-40 object-cover mb-4" />   
      <p className="text-gray-600 mb-4">{purchase.description}</p>
      <div className="flex justify-between items-center mb-4">
        <span className="text-2xl font-bold text-green-600">${purchase.price}</span>
        <span className="text-sm bg-blue-100 text-blue-800 py-1 px-2 rounded-full">
          Qty: {purchase.quantity}
        </span>
      </div>
      <div className="flex items-center justify-between mb-2">
        <StarRating rating={purchase.rate} />
        <div className="mt-4 flex items-center text-sm text-gray-500">
          <Calendar className="w-4 h-4 mr-2" />
          <span>{purchaseDate.toLocaleDateString()}</span>
        </div>
      </div>
      <a
        href={purchase.link}
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-600 hover:underline text-sm"
      >
        View Product
      </a>
    </div>
  </div>
)
}

const PurchasesDisplay = ({ purchases }: { purchases: Purchase[] }) => {
  if (purchases.length === 0) {
    return (
      <div className="text-center py-10">
        <h3 className="text-2xl font-semibold text-gray-700 mb-4">Your Purchases</h3>
        <p className="text-gray-500">No purchases found</p>
      </div>
    )
  }

  return (
    <div className="py-10 px-4 sm:px-6 lg:px-8">
      <h3 className="text-2xl font-semibold text-gray-700 mb-6 text-center">Your Purchases</h3>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {purchases.map((purchase) => (
          <PurchaseCard key={purchase.item_id} purchase={purchase} />
        ))}
      </div>
    </div>
  )
}

export default function PurchasesPage(purchases: Purchase[]) {
    return (
    <div className="min-h-screen bg-gray-100">
      <main className="max-w-7xl mx-auto">
        <PurchasesDisplay purchases={purchases} />
      </main>
    </div>
  )
}

