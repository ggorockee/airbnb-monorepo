import { Grid } from "@chakra-ui/react";
import { useQuery } from "@tanstack/react-query";
import { getRooms } from "../api";
import Room from "../components/Room";
import { IRoomList } from "../types";

export default function Home() {
	const {
		// isLoading은 더 이상 사용하지 않으므로 제거해도 됩니다.
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
			{/*
      데이터 로딩(isLoading) 상태와 관계없이
      rooms 데이터가 있을 때만 Room 컴포넌트를 렌더링합니다.
      초기값으로 빈 배열([])이 설정되어 있어 오류가 발생하지 않습니다.
    */}
			{rooms.map((room) => (
				<Room
					key={room.pk}
					pk={room.pk}
					isOwner={room.is_owner}
					imageUrl={room.photos[0]?.file}
					name={room.name}
					rating={room.rating}
					city={room.city}
					country={room.country}
					price={room.price}
				/>
			))}
		</Grid>
	);
}