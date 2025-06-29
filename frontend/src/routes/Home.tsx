import { Grid } from "@chakra-ui/react";
import { useQuery } from "@tanstack/react-query";
import { getRooms } from "../api";
import Room from "../components/Room";
import RoomSkeleton from "../components/RoomSkeleton";
import { IRoomList } from "../types";

export default function Home() {
	// 1) 제네릭을 <데이터타입, 에러타입> 으로 지정
	// 2) 객체 옵션 형태로 queryKey, queryFn을 명시
	// 3) data를 바로 rooms로 받고 기본값을 빈 배열([])로 설정
	const {
		isLoading,
		data: rooms = [],
		error,
	} = useQuery<IRoomList[], Error>({
		queryKey: ["rooms"],
		queryFn: getRooms,
	});

	if (error) {
		return <p>에러 발생: {error.message}</p>;
	}

	return (
		<Grid
			mt={10}
			px={{ base: 10, lg: 40 }}
			columnGap={4}
			rowGap={8}
			templateColumns={{
				sm: "1fr",
				md: "1fr 1fr",
				lg: "repeat(3, 1fr)",
				xl: "repeat(4, 1fr)",
				"2xl": "repeat(5, 1fr)",
			}}
		>
			{isLoading ? (
				// skeleton 개수만큼 보여주기
				Array.from({ length: 10 }).map((_, i) => <RoomSkeleton key={i} />)
			) : (
				// rooms는 항상 IRoomList[] 이므로 map 사용 가능
				rooms.map((room) => (
					<Room
						key={room.pk}
						pk={room.pk}
						imageUrl={room.photos[0].file}
						name={room.name}
						rating={room.rating}
						city={room.city}
						country={room.country}
						price={room.price}
					/>
				))
			)}
		</Grid>
	);
}
