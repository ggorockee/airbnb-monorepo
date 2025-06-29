import axios from "axios";
import { IRoom } from "./routes/Home"; // IRoom 인터페이스가 있는 곳을 정확히 import

// const instance = axios.create({
// 	baseURL: "http://airbnb-umbrella-dev-backend.airbnb-dev.svc.cluster.local:8000/api/v1/",
// });

const instance = axios.create({
	baseURL: "http://localhost:8000/api/v1/",
});

export const getRooms = () =>
	instance.get("room/").then((response) => response.data);

// 단일 방 조회 — roomPk 를 파라미터로 받도록 수정
export const getRoom = (roomPk: string | number): Promise<IRoom> =>
	instance.get(`room/${roomPk}/`).then((response) => response.data);