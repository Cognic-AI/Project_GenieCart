// firestore.js
import { db } from "../database/firebase_config.js";
import { collection, addDoc, getDocs,setDoc,doc ,getDoc} from "firebase/firestore";

// Add a new document
export const addData = async (collectionName, data) => {
  try {
    const docRef = await addDoc(collection(db, collectionName), data);
    return docRef.id;
  } catch (error) {
    console.error("Error adding document:", error);
    throw error;
  }
};

// Fetch all documents
export const fetchData = async (collectionName) => {
  try {
    const querySnapshot = await getDocs(collection(db, collectionName));
    return querySnapshot.docs.map((doc) => ({ id: doc.id, ...doc.data() }));
  } catch (error) {
    console.error("Error fetching data:", error);
    throw error;
  }
};

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
  
      const items = [];
  
      // Iterate over each document in the 'history' collection
      for (const historyDoc of querySnapshot.docs) {
        const historyItems = historyDoc.get("items"); // Assume 'items' is an array of item IDs
  
        if (Array.isArray(historyItems)) {
          // Sequentially fetch each item
          for (const itemId of historyItems) {
            const itemRef = doc(db, "item", itemId); // Reference to the 'items' document
            const itemDoc = await getDoc(itemRef);
            if (itemDoc.exists()) {
              items.push({ id: itemDoc.id, ...itemDoc.data(),time_stamp:historyDoc.get('timestamp') }); // Add item data with ID
            }
          }
        }
      }
  
      console.log("Fetched Items:", items);
      return items;
    } catch (error) {
      console.error("Error fetching history items:", error);
      throw error;
    }
  };
