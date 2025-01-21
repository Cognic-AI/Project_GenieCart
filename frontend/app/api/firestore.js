// firestore.js
import { db } from "../database/firebase_config.js";
import { collection, getDocs,setDoc,doc ,getDoc, updateDoc} from "firebase/firestore";

export const createAccount = async (collectionName, data) => {
    try {
      const docRef = doc(db, collectionName, data['id']); // Reference to the specific document
      await setDoc(docRef, data); // Create or overwrite the document
      console.log("Document successfully written!");  
      return docRef.id;
    } catch (error) {
      console.error("Error adding document:", error);
      throw error;
    }
  };

  export const fetchProfile = async (collectionName,uid) => {
    try {
      const docRef = await doc(db, collectionName,uid);
      // Fetch the document's data
      const docSnap = await getDoc(docRef);

      if (docSnap.exists()) {
        return docSnap.data(); // Return the document's data
      } else {
        console.error("No such document!");
        return null;
      }
    } catch (error) {
      console.error("Error fetching data:", error);
      throw error;
    }
  };
  export const fetchHistory = async (uid) => {
    try {
      // Fetch all documents in the 'history' subcollection
      const docCollection = collection(db, "customer", uid, "history");
      const querySnapshot = await getDocs(docCollection);

      const docs_ = querySnapshot.docs;
      docs_.sort((a, b) => {
        // Get the timestamps as Firestore Timestamp objects
        const timeA = a.get('timestamp');
        const timeB = b.get('timestamp');
  
        // Convert Firestore Timestamp to Date objects if necessary
        const parseDate = (dateStr) => {
          const [datePart, timePart] = dateStr.split(' '); // Split date and time
          const [year, month, day] = datePart.split('-').map(num => parseInt(num, 10));
          const [hour, minute, second] = timePart.split(':').map(num => parseInt(num, 10));
      
          return new Date(year, month - 1, day, hour, minute, second); // Create a Date object
        };

        // Convert time strings to Date objects
        const dateA = parseDate(timeA);
        const dateB = parseDate(timeB);

        console.log(dateB)
  
        // Sort in descending order by how recent the timestamp is
        return dateB - dateA; // Compare timestamps directly
      });
  
      console.log(docs_);

      const folders = [];
  
      // Iterate over each document in the 'history' collection
      for (const historyDoc of docs_) {
        const folder = {folder:historyDoc.id,items:[]};
        const items = [];
        const historyItems = historyDoc.get("items"); // Assume 'items' is an array of item IDs
        if (Array.isArray(historyItems)) {
          // Sequentially fetch each item
          var count = 0;
          for (const itemId of historyItems) {
            count++;
            const itemRef = doc(db, "item", itemId); // Reference to the 'items' document
            const itemDoc = await getDoc(itemRef);
            if (itemDoc.exists()) {
              items.push({ item_id: itemDoc.id, ...itemDoc.data(),time_stamp:historyDoc.get('timestamp')}); // Add item data with ID
            }
            if(count==3) {
              break;
            }
          }
          folder.items = items;
        }
        folders.push(folder);
      }
  
      console.log("Fetched folders:", folders);
      return folders;
    } catch (error) {
      console.error("Error fetching history items:", error);
      throw error;
    }
  };
  export const updatePriceLevel = async (uid,price_level) => {
    try {
      const docRef = doc(db, "customer", uid); // Reference to the specific document
      await updateDoc(docRef, {
        price_level: price_level // Update the 'price_level' field
      }); // Create or overwrite the document
      console.log("Price level updated successfully!");
      return docRef.id;
    } catch (error) {
      console.error("Error updating price level:", error);
      throw error;
    }
  };

  export const updateName = async (uid,name) => {
    try {
      const docRef = doc(db, "customer", uid); // Reference to the specific document
      await updateDoc(docRef, {
        name: name // Update the 'price_level' field
      }); // Create or overwrite the document
      console.log("Name updated successfully!");
      return docRef.id;
    } catch (error) {
      console.error("Error updating name:", error);
      throw error;
    }
  };

  export const updatePic = async (uid,pic) => {
    try {
      const docRef = doc(db, "customer", uid); // Reference to the specific document
      await updateDoc(docRef, {
        image_link: pic // Update the 'price_level' field
      }); // Create or overwrite the document
      console.log("Image updated successfully!");
      return docRef.id;
    } catch (error) {
      console.error("Error updating image:", error);
      throw error;
    }
  };

  export const fetchPurchases = async (uid) => {
    try {
      // Fetch all documents in the 'history' subcollection
      const docCollection = collection(db, "customer", uid, "purchase");
      const querySnapshot = await getDocs(docCollection);

      const docs_ = querySnapshot.docs;
      docs_.sort((a, b) => {
        // Get the timestamps as Firestore Timestamp objects
        const timeA = a.get('timestamp');
        const timeB = b.get('timestamp');
  
        // Convert Firestore Timestamp to Date objects if necessary
        const parseDate = (dateStr) => {
          const [datePart, timePart] = dateStr.split(' '); // Split date and time
          const [year, month, day] = datePart.split('-').map(num => parseInt(num, 10));
          const [hour, minute, second] = timePart.split(':').map(num => parseInt(num, 10));
      
          return new Date(year, month - 1, day, hour, minute, second); // Create a Date object
        };

        // Convert time strings to Date objects
        const dateA = parseDate(timeA);
        const dateB = parseDate(timeB);

        console.log(dateB)
  
        // Sort in descending order by how recent the timestamp is
        return dateB - dateA; // Compare timestamps directly
      });
  
      console.log(docs_);

      const items = [];
  
      // Iterate over each document in the 'purchased' collection
      for (const purchaseDoc of docs_) {
        const purchaseItem = purchaseDoc.get("item"); 
        const itemRef = doc(db, "item", purchaseItem); // Reference to the 'items' document
        const itemDoc = await getDoc(itemRef);
        if (itemDoc.exists()) {
          items.push({ item_id: itemDoc.id, ...itemDoc.data(),time_stamp:purchaseDoc.get('timestamp') }); // Add item data with ID
        }
      }  
      console.log("Fetched Items:", items);
      return items;
    } catch (error) {
      console.error("Error fetching purchased items:", error);
      throw error;
    }
  };

  export const updateKey = async (uid,key) => {
    try {
      const docRef = doc(db, "customer", uid); // Reference to the specific document
      await updateDoc(docRef, {
        generated_key: key 
      }); // Create or overwrite the document
      console.log("Key updated successfully!");
      return docRef.id;
    } catch (error) {
      console.error("Error updating Key:", error);
      throw error;
    }
  };

  export const updateLocation = async (uid,lat, lon) => {
    try {
      const docRef = doc(db, "customer", uid); // Reference to the specific document
      await updateDoc(docRef, {
        latitude: lat,
        longitude: lon
      }); // Create or overwrite the document
      console.log("Location updated successfully!");
      return docRef.id;
    } catch (error) {
      console.error("Error updating location:", error);
      throw error;
    }
  };