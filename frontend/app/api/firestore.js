// firestore.js
import { db } from "../database/firebase_config.js";
import { collection, addDoc, getDocs } from "firebase/firestore";

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
      const docRef = await addDoc(collection(db, collectionName,data['id']), data);
      return docRef.id;
    } catch (error) {
      console.error("Error adding document:", error);
      throw error;
    }
  };
