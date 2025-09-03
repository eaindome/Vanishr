import api from "./api";

export interface Broker {
  id: string;
  name: string;
  website: string;
  status: string;
}

export const getBrokers = async (): Promise<Broker[]> => {
  const { data } = await api.get("/brokers");
  return data;
};

export const createBroker = async (broker: Partial<Broker>): Promise<Broker> => {
  const { data } = await api.post("/brokers", broker);
  return data;
};

export const deleteBroker = async (id: string): Promise<void> => {
  await api.delete(`/brokers/${id}`);
};
