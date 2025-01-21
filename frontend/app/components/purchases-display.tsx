import { Calendar, Clock, Star } from 'lucide-react';
import { useState } from 'react';

interface Purchase {
  item_id: string;
  name: string;
  description: string;
  price: number;
  link: string;
  rate: number;
  image_link: string;
  timestamp: string;
}

interface Folder {
  folder: string;
  items: Purchase[];
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
  );
};

const PurchaseCard = ({ purchase }: { purchase: Purchase }) => {
  const purchaseDate = new Date(purchase.timestamp);

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden transition-all duration-300 hover:shadow-lg hover:scale-105">
      <div className="p-6">
        <h2
          className="text-xl font-bold mb-2 text-gray-800"
          style={{ color: '#5479f7' }}
        >
          {purchase.name.slice(0, 20)}
        </h2>
        <img
          src={purchase.image_link}
          alt={purchase.name}
          className="w-full h-40 object-cover mb-4"
        />
        <div className="flex justify-between items-center mb-4">
          <span className="text-2xl font-bold text-green-600">
            ${purchase.price}
          </span>
        </div>
        <div className="flex items-center justify-between mb-2">
          <StarRating rating={purchase.rate} />
          <div className="mt-4 flex flex-col items-start text-sm text-gray-500">
            <div className="flex items-center">
              <Calendar className="w-4 h-4 mr-2" />
              <span>{purchaseDate.toLocaleDateString()}</span>
            </div>
            <div className="flex items-center">
              <Clock className="w-4 h-4 mr-2" />
              <span>{purchaseDate.toLocaleTimeString()}</span>
            </div>
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
  );
};

export default function PurchasesPage({
  folders,
  purchases,
  viewMode,
}: {
  folders: Folder[];
  purchases: Purchase[];
  viewMode: 'history' | 'purchase';
}) {
  const [selectedFolder, setSelectedFolder] = useState<Purchase[] | null>(null);
  const [selectedFolderName, setSelectedFolderName] = useState<string | null>(
    null
  );

  return (
    <div className="min-h-screen bg-gray-100 w-full">
      <main className="max-w-7xl mx-auto w-full py-10 px-4 sm:px-6 lg:px-8">
        {viewMode === 'history' ? (
          <div className="flex space-x-6">
            {/* Left Sidebar for Folders */}
            <div className="w-1/3 bg-gray-100 rounded-lg p-4">
              <h2 className="text-lg font-bold text-gray-600 mb-4">Folders</h2>
              {folders.map((folder) => (
                <div
                  key={folder.folder}
                  className={`bg-white p-4 rounded-md shadow cursor-pointer hover:bg-gray-50 ${
                    selectedFolderName === folder.folder
                      ? 'bg-blue-100 border-blue-400 border'
                      : ''
                  }`}
                  style={{ marginBottom: 10 }}
                  onClick={() => {
                    setSelectedFolder(folder.items);
                    setSelectedFolderName(folder.folder);
                  }}
                >
                  <h2
                    className="font-bold text-blue-600"
                    style={{ overflow: 'clip' }}
                  >
                    {folder.folder}
                  </h2>
                </div>
              ))}
            </div>

            {/* Right Content for Selected Folder */}
            <div className="w-2/3">
              {selectedFolder ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                  {selectedFolder.map((purchase) => (
                    <PurchaseCard key={purchase.item_id} purchase={purchase} />
                  ))}
                </div>
              ) : (
                <div className="text-center py-10">
                  <p className="text-gray-500" style={{ color: '#5479f7' }}>
                    Select a folder to view purchases.
                  </p>
                </div>
              )}
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
            {purchases.map((purchase) => (
              <PurchaseCard key={purchase.item_id} purchase={purchase} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
