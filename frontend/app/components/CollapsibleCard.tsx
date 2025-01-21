import { ArrowDown, ArrowUp} from 'lucide-react';
import { useState } from 'react';

const CollapsibleCard = () => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [formData, setFormData] = useState({
    secretKey: '',
    itemName: '',
    tags: '',
    price_level:'',
    onlySyscolab: false,
  });
  const toggleCard = () => {
    setIsExpanded(!isExpanded);
  };
  const handleChanges = (e) =>{
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };
  const send =async () => {
    // alert(JSON.stringify(submittedData));
    try {
        // Generate a dynamic Bearer token (replace this logic with actual token generation logic if needed)
        const token = `Bearer ${Math.random().toString(36).substring(7)}`; 
    
        // Create the request body
        const body = {
          secret_key: formData.secretKey,
          item_name: formData.itemName,
          tags: formData.tags.split(" "),
          price_level: formData.price_level=="High"?1:(formData.price_level=="Middle"?2:3),
          custom_domains: formData.onlySyscolab
            ? ["https://www.amazon.com"]
            : null,
        };
    
        // Make the POST request
        const response = await fetch("http://localhost:8000/api/recommend", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body),
        });
    
        // Handle the response
        if (response.ok) {
          const data = await response.json();
          alert(`Response: ${JSON.stringify(data)}`);
          setFormData({
            secretKey: "",
            itemName: "",
            tags: "",
            onlySyscolab: false,
            price_level: "",
          }); // Reset form
        } else {
          const error = await response.json();
          alert(`Error: ${JSON.stringify(error)}`);
        }
      } catch (err) {
        alert(`Error: ${err.message}`);
      }
  };

  return (
    <div
      className="absolute top-8 right-8 p-4 shadow-lg rounded-lg"
      style={{
        width: '20vw',
        backgroundColor: 'white',
        border: '1px solid #ddd',
        overflow: 'hidden',
        transition: 'height 0.3s ease',
        height: isExpanded ? 'auto' : '3rem', // Dynamic height
      }}
    >
      {/* Card Header */}
      <div
        className="flex items-center justify-between cursor-pointer"
        onClick={toggleCard}
      >
        <div className="flex items-center space-x-2">
          {/*<div
            className="p-2 rounded-full bg-blue-100"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <img
              src="https://via.placeholder.com/24" // Replace with your icon's source
              alt="Electrical Item Icon"
            />
          </div>*/}
          <h2 className="text-lg font-semibold text-gray-800">Demo API Call</h2>
        </div>
            <span className="text-xl font-bold text-gray-600">
                {isExpanded ? <ArrowUp /> : <ArrowDown />}
            </span>
      </div>

      {/* Card Content */}
      {isExpanded && (
        <div className="mt-4 space-y-4">
          <input
            type="text"
            name="secretKey" 
            placeholder="Secret Key"
            required
            className="border rounded-md p-2 w-full"
            value={formData.secretKey}
            onChange={handleChanges}
          />
          <input
            type="text"
            name="itemName"
            placeholder="Item Name"
            required
            className="border rounded-md p-2 w-full"
            value={formData.itemName}
            onChange={handleChanges}
          />
          <input
            type="text"
            name="tags"
            placeholder="Tags/Description"
            className="border rounded-md p-2 w-full"
            value={formData.tags}
            onChange={handleChanges}
          />
          <select
            name="price_level"
            className="border rounded-md p-2 w-full"
            value={formData.price_level}
            onChange={handleChanges}
            >
            <option value="">Select Priority</option>
            <option value="High">High</option>
            <option value="Middle">Middle</option>
            <option value="Low">Low</option>
            </select>

          <div className="flex items-center space-x-2">
            <input type="checkbox" id="syscolab" className="form-checkbox" onChange={handleChanges} checked={formData.onlySyscolab} name='onlySyscolab'/>
            <label htmlFor="syscolab" className="text-sm text-gray-600">
              Only Amazon products
            </label>
          </div>
          <button
            className="bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition duration-300 w-full"
            style={{ backgroundColor: '#5479f7'}}
            onClick={send}
          >
            Send
          </button>
        </div>
      )}
    </div>
  );
};

export default CollapsibleCard;
